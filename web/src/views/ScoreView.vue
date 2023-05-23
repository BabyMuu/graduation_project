<script setup>
import {RefreshRight} from '@element-plus/icons-vue'
import {Search} from '@element-plus/icons-vue'
</script>
<template>
  <br>
  <!-- 表格头开始 -->
  <div style="margin-left: 10%">
    <el-button type="primary" :icon="RefreshRight" circle
               @click="this.getFormValue(this.currentUserPage); "/>&nbsp;
    <el-button type="primary" @click="this.getAll()">获取全部成绩</el-button>&nbsp;
    <el-button type="danger" @click="this.createFormVisible=true">批量删除</el-button>
    <div style="float: right; display: inline; margin-right: 13%">
      <el-input
          v-model="searchBy"
          placeholder="请输入学生姓名"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch"/>
        </template>
      </el-input>
    </div>
  </div>
  <br>
  <!-- 表格头结束 -->
  <!-- 表格开始 -->
  <el-table :data="scores"
            :header-cell-style="{'text-align':'center'}"
            :cell-style="{'text-align':'center'}"
            border style="width: 90%; margin-left: 5%;"
            @selection-change="UserSelectionChange"
  >
    <el-table-column type="selection" width="55"/>
    <el-table-column label="#" type="index" width="60"/>
    <el-table-column label="考试ID" width="80">
      <template #default="scope">
        <div>
          <el-tag>{{ scope.row.exam_id }}</el-tag>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="学生姓名" width="100">
      <template #default="scope">
        {{ scope.row.stu_name }}
      </template>
    </el-table-column>

    <el-table-column label="总分" width="80">
      <template #default="scope">
        <div>
          <span>{{ scope.row.score }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="各题得分情况" width="380">
      <template #default="scope">
        <div>
          <span>{{ scope.row.score_situation }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="掌握知识点">
      <template #default="scope">
        <div>
          <span>{{ scope.row.score_know_situation }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="200">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
        >数据分析图
        </el-button>
        <el-popconfirm width="80" title="Are you sure to delete this?" @confirm="handleDelete(scope.$index, scope.row)">
          <template #reference>
            <el-button
                size="small"
                type="danger"
            >Delete
            </el-button>
          </template>
        </el-popconfirm>
      </template>
    </el-table-column>
  </el-table>
  <!-- 表格结束 -->
  <!-- 分页开始 -->
  <br><br><br>
  <el-pagination
      v-model:currentPage="currentUserPage"
      :page-size="pageSize"
      layout="total, prev, pager, next"
      style="text-align: center; float: bottom; margin-left: 30%"
      :total="rolesTotal"
      @current-change="getFormValue"
  />
  <!-- 分页结束 -->
  <!-- 学生个人知识点数据分析图开始 -->
  <el-dialog v-model="editFormVisible" title="学生单次考试个人知识点数据分析折线图">
    <div id="charts" style="width: 800px; height:400px"/>
  </el-dialog>
  <!-- 学生个人知识点数据分析图结束 -->

</template>

<script>
import axios from "axios";
import {ElMessage} from "element-plus";
import * as echarts from 'echarts';
import * as $echart from "echarts";

export default {
  data() {
    return {
      searchBy: "",
      pageSize: 15,
      rolesTotal: 1000,
      currentUserPage: 1,
      editFormVisible: false,
      createFormVisible: false,
      editForm: {},
      createForm: {},
      defaultCreateForm: {
        level: '',
        name: '',
        info: '',
      },
      query_id: '',
      scores: [],
      know_situation_ana: {
        'know_points': [],
        'levels': []
      },
      stu_name: [],
      chart_data: {}
    }
  },
  mounted() {
    this.query_id = this.$route.query.id
    if (this.query_id !== '') {
      this.getFormValue(1)
    }
  },
  methods: {
    getAll() {
      this.query_id = ''
      this.searchBy = ''
      this.getFormValue(1)
    },

    handleSearch() {
      this.getFormValue(1)
    },
    UserSelectionChange() {

    },
    handleDelete(row, data) {
      axios.delete("user/users", {
        params: {
          userId: 1,
          id: data.id
        }
      }).then(
          res => {
            ElMessage.success("删除成功")
            this.getFormValue(this.currentUserPage)
          }
      ).catch(
          err => {
            ElMessage.success("删除失败!", err.response.msg)
          }
      )

    },
    getFormValue(pageNum) {
      if (this.searchBy !== '') {
        this.query_id = ''
      }
      axios.get("user/scores/",
          {
            params: {
              page: pageNum,
              student_id: this.query_id,
              stu_name: this.searchBy
            }
          }).then(response => {
        this.scores = response.data.results
        this.rolesTotal = response.data.count
      }).catch(
          err => {
            console.log(err.response)
            ElMessage.error("查找失败! " + err.response.data.msg)
          }
      )
    },
    get_charts() {
      let chartDomSales = document.getElementById("charts");
      let myChart = $echart.init(chartDomSales);
      let option = {
        title: {
          text: 'Stacked Line'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: this.stu_name
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: true,
          axisLabel: {
            //x轴文字的配置
            show: true,
            interval: 0,//使x轴文字显示全
          },
          data: this.know_situation_ana['know_points']
        },
        yAxis: {
          data: ['差', '中', '良', '优']
        },
        series: [
          {
            name: this.stu_name[0],
            type: 'line',
            stack: 'Total',
            data: this.know_situation_ana['levels']
          },

        ]
      };
      option && myChart.setOption(option);
      window.addEventListener("resize", function () {
        myChart.resize();
      });
    },
    handleEdit(index, row) {
      console.log("rooo", index, row)
      axios.get(
          "ana/student_analysis/?stu_id=" + row.student_id + "&exam_id=" + row.exam_id
      ).then(
          res => {
            this.know_situation_ana = res.data
            this.stu_name = [row.stu_name]
            console.log("stu_name", this.stu_name)
            // 绘制图表

            this.editFormVisible = true;
            setTimeout(() => {
              this.get_charts();
            }, 1);
          }
      )
    },
  },
  created() {
    if (this.query_id !== '' && this.searchBy !== '') {
      this.getFormValue(1)
    }
  }
}


</script>

<style scoped>

</style>