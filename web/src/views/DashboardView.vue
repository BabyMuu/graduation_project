<script setup>
import {Timer, List, TrendCharts, User} from '@element-plus/icons-vue'
</script>
<template>
  <div class="default-main">
    <div class="banner">
      <el-row :gutter="10">
        <el-col :md="24" :lg="18">
          <div class="welcome suspension">
            <img class="welcome-img" src="@/assets/logo.png" alt="welcome logo"/>
            <div class="welcome-text">
              <div class="welcome-title">{{ username }}, 下午好, 欢迎回来</div>
              <div class="welcome-note">
                开源等于互助；开源需要大家一起来支持，支持的方式有很多种，比如使用、推荐、写教程、保护生态、贡献代码、回答问题、分享经验、打赏赞助等；欢迎您加入我们！
              </div>
            </div>
          </div>
        </el-col>
        <el-col :lg="6" class="hidden-md-and-down">
          <div class="working">
            <img class="working-coffee" src="@/assets/dashboard/coffee.svg" alt=""/>
            <div class="working-text">
              {{ '您今天已经工作了' }}<span class="time">{{ state.workingTimeFormat }}</span>
            </div>
            <div @click="onChangeWorkState()" class="working-opt working-rest">
              {{ state.pauseWork ? '继续工作' : '休息片刻' }}
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="small-panel-box">
      <el-row :gutter="20">
        <el-col :sm="12" :lg="6">
          <div class="small-panel user-reg suspension">
            <div class="small-panel-title">会员新增量</div>
            <div class="small-panel-content">
              <div class="content-left">
                <el-icon size="40px">
                  <Timer/>
                </el-icon>
                <span id="user_reg_number" style="margin-left: 10px; font-size: 40px">{{ this.userReg }}</span>
              </div>
              <div class="content-right">+{{ this.userRegPoint * 100 }}%</div>
            </div>
          </div>
        </el-col>
        <el-col :sm="12" :lg="6">
          <div class="small-panel file suspension">
            <div class="small-panel-title">会员总数</div>
            <div class="small-panel-content">
              <div class="content-left">
                <el-icon size="40px">
                  <User/>
                </el-icon>
                <span id="file_number" style="margin-left: 10px; font-size: 40px">{{ this.userTotal }}</span>
              </div>
              <div class="content-right">+{{ this.userTotalPoint * 100 }}%</div>
            </div>
          </div>
        </el-col>
        <el-col :sm="12" :lg="6">
          <div class="small-panel users suspension">
            <div class="small-panel-title">新增订单数量</div>
            <div class="small-panel-content">
              <div class="content-left">
                <el-icon size="40px">
                  <TrendCharts/>
                </el-icon>
                <span id="users_number" style="margin-left: 10px; font-size: 40px">{{ this.orderReg }}</span>
              </div>
              <div class="content-right">+{{ this.orderRegPoint * 100 }}%</div>
            </div>
          </div>
        </el-col>
        <el-col :sm="12" :lg="6">
          <div class="small-panel addons suspension">
            <div class="small-panel-title">订单总数</div>
            <div class="small-panel-content">
              <div class="content-left">
                <el-icon size="40px">
                  <List/>
                </el-icon>
                <span id="addons_number" style="margin-left: 10px; font-size: 40px">{{ this.orderTotal }}  </span>
              </div>
              <div class="content-right">+{{ this.orderTotalPoint * 100 }}%</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="growth-chart">
      <el-row :gutter="20">
        <el-col class="lg-mb-20" :xs="24" :sm="24" :md="12" :lg="9">
          <el-card shadow="hover">
            <div class="user-growth-chart" id="dailySales"></div>
          </el-card>
        </el-col>
        <el-col class="lg-mb-20" :xs="24" :sm="24" :md="12" :lg="9">
          <el-card shadow="hover">
            <div class="user-growth-chart" id="dailyUsers"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="24" :md="24" :lg="6">
          <el-card class="new-user-card" shadow="hover" :header="会员增长情况">
            <div class="new-user-growth">
              <el-scrollbar>
                <div class="new-user-item" v-for="(user,index) in users">
                  <img class="new-user-avatar" :src="user.icon" alt=""/>
                  <div class="new-user-base">
                    <div class="new-user-name">{{ user.username }}</div>
                    <div class="new-user-time">{{ user.difTime }}分钟前加入我们</div>
                  </div>
                  <Icon class="new-user-arrow" color="#8595F4" name="fa fa-angle-right"/>
                </div>
              </el-scrollbar>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div class="growth-chart">
      <el-row :gutter="20">
        <el-col class="lg-mb-20" :xs="24" :sm="24" :md="24" :lg="12">
          <el-card shadow="hover" :header="会员来源">
            <div class="user-surname-chart" id="orderStat"></div>
          </el-card>
        </el-col>
        <el-col class="lg-mb-20" :xs="24" :sm="24" :md="24" :lg="12">
          <el-card shadow="hover" :header="会员姓氏">
            <div class="user-surname-chart" id="orderTotal"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import {mapState} from "vuex";
import * as echarts from 'echarts';

export default {
  data() {
    return {
      d: new Date(),
      orderTotal: 0,  // 订单总数
      orderReg: 0,  // 最近订单数
      userTotal: 0, // 用户总数
      userReg: 0,  // 最近注册用户人数
      orderTotalPoint: 0,
      orderRegPoint: 0,
      userTotalPoint: 0,
      userRegPoint: 0,
      workTimer: "",
      state: {
        workingTimeFormat: '',
        pauseWork: false,
      },
      users: [
        {
          username: "妙笔生花",
          difTime: 12,
          icon: "",
        },
        {
          username: "妙笔生花",
          difTime: 12,
          icon: "",
        }, {
          username: "妙笔生花",
          difTime: 12,
          icon: "",
        }
      ],
      chartData: [{}, {}, {}, {}],
      userInfo: {},
    }
  },
  computed: {
    ...mapState(['username']),
  },
  methods: {
    get_data() {
      axios.get("dashboard").then(
          res => {
            let data = res.data.data
            this.orderTotal = data.orderTotal
            this.orderReg = data.orderReg
            this.userTotal = data.userTotal
            this.userReg = data.userReg
            this.orderTotalPoint = data.orderTotalPoint
            this.orderRegPoint = data.orderRegPoint
            this.userTotalPoint = data.userTotalPoint
            this.userRegPoint = data.userRegPoint
            this.users = data.users
            let userChart = {
              title: {
                text: '近三十天订单数'
              },
              tooltip: {
                trigger: 'axis'
              },
              legend: {},
              toolbox: {
                show: true,
                feature: {
                  dataZoom: {
                    yAxisIndex: 'none'
                  },
                  dataView: {readOnly: false},
                  magicType: {type: ['line', 'bar']},
                  restore: {},
                  saveAsImage: {}
                }
              },
              xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data.chartData.user.date.reverse()
              },
              yAxis: {
                type: 'value',
                axisLabel: {
                  formatter: '{value} 人'
                }
              },
              series: [
                {
                  name: 'Highest',
                  type: 'line',
                  data: data.chartData.user.stat.reverse(),
                  markPoint: {
                    data: [
                      {type: 'max', name: 'Max'},
                      {type: 'min', name: 'Min'}
                    ]
                  },
                  markLine: {
                    data: [{type: 'average', name: 'Avg'}]
                  }
                },
              ],
              grid: { // 让图表占满容器
                top: "70px",
                bottom: "20px"
              }
            }
            let orderChart = {
              title: {
                text: '近三十天订单数'
              },
              tooltip: {
                trigger: 'axis'
              },
              legend: {},
              toolbox: {
                show: true,
                feature: {
                  dataZoom: {
                    yAxisIndex: 'none'
                  },
                  dataView: {readOnly: false},
                  magicType: {type: ['line', 'bar']},
                  restore: {},
                  saveAsImage: {}
                }
              },
              xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data.chartData.order.date.reverse()
              },
              yAxis: {
                type: 'value',
                axisLabel: {
                  formatter: '{value} 单'
                }
              },
              series: [
                {
                  name: 'Highest',
                  type: 'line',
                  data: data.chartData.order.stat.reverse(),
                  markPoint: {
                    data: [
                      {type: 'max', name: 'Max'},
                      {type: 'min', name: 'Min'}
                    ]
                  },
                  markLine: {
                    data: [{type: 'average', name: 'Avg'}]
                  }
                },
              ],
              grid: { // 让图表占满容器
                top: "70px",
                bottom: "20px"
              }
            }
            let orderStatChart = {
              title: {
                text: '商品品类销量'
              },
              tooltip: {
                trigger: 'item'
              },
              legend: {
                top: '5%',
                left: 'center'
              },
              series: [
                {
                  name: 'Access From',
                  type: 'pie',
                  radius: ['40%', '70%'],
                  avoidLabelOverlap: false,
                  itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                  },
                  label: {
                    show: false,
                    position: 'center'
                  },
                  emphasis: {
                    label: {
                      show: true,
                      fontSize: '40',
                      fontWeight: 'bold'
                    }
                  },
                  labelLine: {
                    show: false
                  },
                  data: [
                    data.chartData.orderStat
                  ]
                }
              ]
            }
            let orderTotalChart = {
              title: {
                text: '商品月销量'
              },
              tooltip: {
                trigger: 'axis'
              },
              legend: {},
              toolbox: {
                show: true,
                feature: {
                  dataZoom: {
                    yAxisIndex: 'none'
                  },
                  dataView: {readOnly: false},
                  magicType: {type: ['line', 'bar']},
                  restore: {},
                  saveAsImage: {}
                }
              },
              xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data.chartData.orderTotal.date.reverse()
              },
              yAxis: {
                type: 'value',
                axisLabel: {
                  formatter: '{value} 单'
                }
              },
              series: [
                {
                  name: 'Highest',
                  type: 'line',
                  data: data.chartData.orderTotal.stat.reverse(),
                  markPoint: {
                    data: [
                      {type: 'max', name: 'Max'},
                      {type: 'min', name: 'Min'}
                    ]
                  },
                  markLine: {
                    data: [{type: 'average', name: 'Avg'}]
                  }
                },
              ],
              grid: { // 让图表占满容器
                top: "70px",
                bottom: "20px"
              }
            }
            this.chartData[0] = userChart
            this.chartData[1] = orderChart
            this.chartData[2] = orderStatChart
            this.chartData[3] = orderTotalChart
            this.get_charts()
          }
      )
      console.log("get_data")
    },
    get_charts() {
      console.log("userINfo", this.userInfo)
      let chartDomSales = document.getElementById('dailySales');
      let myChart = echarts.init(chartDomSales);
      let option = this.chartData[0]
      option && myChart.setOption(option);
      let chartDomUsers = document.getElementById('dailyUsers');
      myChart = echarts.init(chartDomUsers);
      option = this.chartData[1]
      option && myChart.setOption(option);
      let chartDomOrderStat = document.getElementById('orderStat');
      myChart = echarts.init(chartDomOrderStat);
      option = this.chartData[2]
      option && myChart.setOption(option);
      let chartDomOrderTotal = document.getElementById('orderTotal');
      myChart = echarts.init(chartDomOrderTotal);
      option = this.chartData[3]
      option && myChart.setOption(option);
    },

    onChangeWorkState() {
      console.log(this.workTimer)
      const time = parseInt((new Date().getTime() / 1000).toString())
      const workingTime = JSON.parse(localStorage.getItem('work_time'))
      if (this.state.pauseWork) {
        // 继续工作
        workingTime.pauseTime += time - workingTime.startPauseTime
        workingTime.startPauseTime = 0
        localStorage.setItem('work_time', JSON.stringify(workingTime))
        this.state.pauseWork = false
        this.startTime()
      } else {
        // 暂停工作
        workingTime.startPauseTime = time
        localStorage.setItem("work_time", JSON.stringify(workingTime))
        clearInterval(this.workTimer)
        this.state.pauseWork = true
      }
    },


    startTime() {
      const workingTime = JSON.parse(localStorage.getItem('work_time')) === null ? {
        date: '',
        startTime: 0,
        pauseTime: 0,
        startPauseTime: 0
      } : JSON.parse(localStorage.getItem('work_time'))
      const currentDate = this.d.getFullYear() + '-' + (this.d.getMonth() + 1) + '-' + this.d.getDate()
      const time = parseInt((new Date().getTime() / 1000).toString())

      if (workingTime.date !== currentDate) {
        workingTime.date = currentDate
        workingTime.startTime = time
        workingTime.pauseTime = workingTime.startPauseTime = 0
        localStorage.setItem('work_time', JSON.stringify(workingTime))
      }

      let startPauseTime = 0
      if (workingTime.startPauseTime <= 0) {
        this.state.pauseWork = false
        startPauseTime = 0
      } else {
        this.state.pauseWork = true
        startPauseTime = time - workingTime.startPauseTime // 已暂停时间
      }

      let workingSeconds = time - workingTime.startTime - workingTime.pauseTime - startPauseTime

      this.state.workingTimeFormat = this.formatSeconds(workingSeconds)
      if (!this.state.pauseWork) {
        this.workTimer = setInterval(() => {
          workingSeconds++
          this.state.workingTimeFormat = this.formatSeconds(workingSeconds)
        }, 1000)
      }
    },
    formatSeconds(seconds) {
      let secondTime = 0
      let minuteTime = 0
      let hourTime = 0
      let dayTime = 0
      let result = ''
      if (seconds < 60) {
        secondTime = seconds
      } else {
        // 获取分钟，除以60取整数，得到整数分钟
        minuteTime = Math.floor(seconds / 60)
        // 获取秒数，秒数取佘，得到整数秒数
        secondTime = Math.floor(seconds % 60)
        // 如果分钟大于60，将分钟转换成小时
        if (minuteTime >= 60) {
          // 获取小时，获取分钟除以60，得到整数小时
          hourTime = Math.floor(minuteTime / 60)
          // 获取小时后取佘的分，获取分钟除以60取佘的分
          minuteTime = Math.floor(minuteTime % 60)
          if (hourTime >= 24) {
            // 获取天数， 获取小时除以24，得到整数天
            dayTime = Math.floor(hourTime / 24)
            // 获取小时后取余小时，获取分钟除以24取余的分；
            hourTime = Math.floor(hourTime % 24)
          }
        }
      }

      result =
          hourTime +
          '小时' +
          ((minuteTime >= 10 ? minuteTime : '0' + minuteTime) + '分钟') +
          ((secondTime >= 10 ? secondTime : '0' + secondTime) + '秒')
      if (dayTime > 0) {
        result = dayTime + '天' + result
      }
      return result
    }
  },
  mounted() {
    this.get_data()
    this.startTime()
  },
  created() {

  }
}
</script>
<style scoped lang="scss">
.default-main {
  margin: var(--ba-main-space) var(--ba-main-space) 60px var(--ba-main-space);
}

.welcome {
  transition: all 0.3s ease;
  background: #e1eaf9;
  border-radius: 6px;
  display: flex;
  align-items: center;
  padding: 15px 20px !important;
  box-shadow: 0 0 30px 0 rgba(82, 63, 105, 0.05);

  .welcome-img {
    height: 100px;
    margin-right: 10px;
    user-select: none;
  }

  .welcome-title {
    font-size: 1.5rem;
    line-height: 30px;
    color: var(--ba-color-primary-light);
  }

  .welcome-note {
    padding-top: 6px;
    font-size: 15px;
    color: var(--el-text-color-primary);
  }
}

.working {
  height: 130px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  height: 100%;
  position: relative;

  &:hover {
    .working-coffee {
      -webkit-transform: translateY(-4px) scale(1.02);
      -moz-transform: translateY(-4px) scale(1.02);
      -ms-transform: translateY(-4px) scale(1.02);
      -o-transform: translateY(-4px) scale(1.02);
      transform: translateY(-4px) scale(1.02);
      z-index: 999;
    }
  }

  .working-coffee {
    transition: all 0.3s ease;
    width: 80px;
  }

  .working-text {
    display: block;
    width: 100%;
    font-size: 15px;
    text-align: center;
    color: var(--el-text-color-primary);
  }

  .working-opt {
    position: absolute;
    top: -40px;
    right: 10px;
    background-color: rgba($color: #000000, $alpha: 0.3);
    padding: 10px 20px;
    border-radius: 20px;
    color: var(--ba-bg-color-overlay);
    transition: all 0.3s ease;
    cursor: pointer;
    opacity: 0;
    z-index: 999;

    &:active {
      background-color: rgba($color: #000000, $alpha: 0.6);
    }
  }

  &:hover {
    .working-opt {
      opacity: 1;
      top: 0;
    }

    .working-done {
      opacity: 1;
      top: 50px;
    }
  }
}

.small-panel-box {
  margin-top: 20px;
}

.small-panel {
  background-color: #e9edf2;
  border-radius: var(--el-border-radius-base);
  transition: all 0.3s ease;
  padding: 25px;
  margin-bottom: 20px;

  .small-panel-title {
    color: #92969a;
    font-size: 15px;
  }

  .small-panel-content {
    display: flex;
    align-items: flex-end;
    margin-top: 20px;
    color: #2c3f5d;

    .content-left {
      font-size: 24px;

      .icon {
        margin-right: 10px;
      }

      span {
        display: inline-block;
        font-size: 28px;
      }
    }

    .content-right {
      font-size: 18px;
      margin-left: auto;
    }

    .color-success {
      color: var(--el-color-success);
    }

    .color-warning {
      color: var(--el-color-warning);
    }

    .color-danger {
      color: var(--el-color-danger);
    }

    .color-info {
      color: var(--el-text-color-secondary);
    }
  }
}

.growth-chart {
  margin-bottom: 20px;
}

.suspension:hover {
  -webkit-transform: translateY(-4px) scale(1.02);
  -moz-transform: translateY(-4px) scale(1.02);
  -ms-transform: translateY(-4px) scale(1.02);
  -o-transform: translateY(-4px) scale(1.02);
  transform: translateY(-4px) scale(1.02);
  -webkit-box-shadow: 0 14px 24px rgba(0, 0, 0, 0.2);
  box-shadow: 0 14px 24px rgba(0, 0, 0, 0.2);
  z-index: 999;
  border-radius: 6px;
}

.user-growth-chart,
.file-growth-chart {
  height: 260px;

}

.new-user-growth {
  height: 300px;
}

.user-source-chart,
.user-surname-chart {
  height: 400px;
}

.new-user-item {
  display: flex;
  align-items: center;
  padding: 20px;
  margin: 10px 15px;
  box-shadow: 0 0 30px 0 rgba(82, 63, 105, 0.05);
  background-color: var(--ba-bg-color-overlay);

  .new-user-avatar {
    height: 48px;
    width: 48px;
    border-radius: 50%;
  }

  .new-user-base {
    margin-left: 10px;
    color: #2c3f5d;

    .new-user-name {
      font-size: 15px;
    }

    .new-user-time {
      font-size: 13px;
    }
  }

  .new-user-arrow {
    margin-left: auto;
  }
}

.new-user-card :deep(.el-card__body) {
  padding: 0;
}

@media screen and (max-width: 425px) {
  .welcome-img {
    display: none;
  }
}

@media screen and (max-width: 1200px) {
  .lg-mb-20 {
    margin-bottom: 20px;
  }
}

html.dark {
  .welcome {
    background-color: var(--ba-bg-color-overlay);
  }

  .small-panel {
    background-color: var(--ba-bg-color-overlay);

    .small-panel-content {
      color: var(--el-text-color-regular);
    }
  }

  .new-user-item {
    .new-user-base {
      color: var(--el-text-color-regular);
    }
  }
}
</style>
