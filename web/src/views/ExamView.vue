<script setup>
import {Timer} from '@element-plus/icons-vue'
import {Phone} from '@element-plus/icons-vue'
import {RefreshRight} from '@element-plus/icons-vue'
import {Search} from '@element-plus/icons-vue'
</script>
<template>
  <div>
    <br>
    <!-- 表格头开始 -->
    <div style="margin-left: 10%">
      <el-button type="primary" :icon="RefreshRight" circle
                 @click="this.getFormValue(this.currentExamPage); "/>&nbsp;
      <el-button type="primary" @click="newUser">新增用户</el-button>&nbsp;
      <el-button type="danger" @click="this.createFormVisible=true">批量删除</el-button>
      <div style="float: right; display: inline; margin-right: 13%">
        <el-input
            v-model="searchBy"
            placeholder="Please input username"
        >
          <template #append>
            <el-button @click="this.searchBy=''">清空</el-button>
            &nbsp; | &nbsp;&nbsp;
            <el-button :icon="Search" @click="this.getFormValue(1)"/>
          </template>
        </el-input>
      </div>
    </div>
    <br>
    <!-- 表格头结束 -->
    <!-- 表格开始 -->
    <el-table
        :data="exams"
        style="width: 80%; margin-bottom: 20px; margin-left: 10%"
        row-key="id"
        border
        default-expand-all

    >
      <el-table-column prop="id" label="标题" sortable width="80"/>
      <el-table-column prop="name" label="名称" sortable width="180"/>
      <el-table-column prop="avg_score" label="平均分" sortable width="200"/>
      <el-table-column prop="min_score" label="最低分" sortable width="180"/>
      <el-table-column prop="max_score" label="最高分" sortable width="180"/>
      <!--      <el-table-column label="状态" width="113">-->
      <!--        <template #default="scope">-->
      <!--          <div>-->
      <!--            <el-tag type="success" v-if="!scope.delete">启用</el-tag>-->
      <!--            <el-tag type="danger" v-if="scope.delete">禁用</el-tag>-->
      <!--          </div>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <!--      <el-table-column label="创建时间" width="180">-->
      <!--        <template #default="scope">-->
      <!--          <div>-->
      <!--            <el-icon>-->
      <!--              <phone/>-->
      <!--            </el-icon>-->
      <!--            <span style="margin-left: 10px">{{ scope.row.createTime }}</span>-->
      <!--          </div>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column label="最后更新时间" width="220">
        <template #default="scope">
          <div>
            <el-icon>
              <timer/>
            </el-icon>
            <span style="margin-left: 10px">{{
                $moment(new Date(scope.row.update_time)).format('YYYY-MM-DD HH:mm:ss')
              }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280">
        <template #default="scope">
          <el-button size="small" @click="handleUpdate(scope.$index, scope.row)"
          >获取最新成绩
          </el-button>
          <el-button size="small" type="success" @click="handleAnalysis(scope.$index, scope.row)"
          >知识点相关度分析
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--  表格结束  -->
    <!-- 分页开始 -->
    <br><br><br>
    <el-pagination
        v-model:currentPage="currentExamPage"
        :page-size="pageSize"
        layout="total, prev, pager, next"
        style="text-align: center; float: bottom; margin-left: 30%"
        :total="examsTotal"
        @current-change="getFormValue"
    />
    <!-- 分页结束 -->
    <!-- 考试知识点相关度数据分析图开始 -->
    <el-dialog v-model="anaFormVisible" :title="this.title" width="1366px">
      <div id="charts" style="width: 1366px; height: 768px"/>
    </el-dialog>
    <!-- 考试知识点相关度数据分析图结束 -->
  </div>
</template>

<script>
import axios from "axios";
import jquery from 'jquery'
import * as $echart from "echarts";

export default {
  name: "PermissionView",
  data() {
    return {
      exams: [],
      pageSize: 15,
      examsTotal: 1000,
      currentExamPage: 1,
      anaFormVisible: false,
      data: [[]],
      title: '',
      graph: {
        data: [],
        links: []
      },
    }
  },
  methods: {
    getFormValue(pageNum) {
      axios.get("ana/exam/?page=" + pageNum,
          {}).then(response => {
        this.exams = response.data.results
        this.examsTotal = response.data.count
      })
    },
    data2Graph() {
      let data = this.data
      let vertices = {}
      let links = [];
      for (let i = 0; i < data.length; i++) {
        let s = String(data[i][0]);
        let t = String(data[i][1]);
        let v = data[i][2];
        vertices[s] = s;
        vertices[t] = t;
        links.push({'source': s, 'target': t, 'value': v});
      }
      let nodes = [];
      jquery.each(vertices, function (k, v) {
        nodes.push({'name': v, 'value': v, 'x': parseInt(Math.random() * 1000), 'y': parseInt(Math.random() * 1000)})
      });
      this.graph['links'] = links;
      this.graph['data'] = nodes;
      this.drawGraph()
    },
    drawGraph() {
      let chartDomSales = document.getElementById("charts");
      let myChart = $echart.init(chartDomSales);
      console.log(this.graph)
      console.log("hello world")
      let option = {
        tooltip: {},
        color: ['#83e0ff', '#45f5ce'],
        series: [
          {
            type: 'graph',
            layout: 'force',
            symbolSize: 60,
            edgeSymbol: ['circle', 'arrow'],
            data: this.graph.data,
            links: this.graph.links,
            roam: true,
            label: {
              show: true,
              formatter: function (e) {
                return e['value'];
              },
              color: 'red'
            },
            edgeLabel: {
              normal: {
                show: true,
                // position: 'left',
                formatter: function (e) {
                  return e['value'];
                },
                fontSize: 20
              }
            },
            force: {
              repulsion: 6000,
              edgeLength: 300
            },
            lineStyle: {
              opacity: 0.9,
              width: 1,
              curveness: 0.1
            }
          }
        ]
      };
      myChart.setOption(option);
      myChart.on('mouseup', function (params) {
        let option = myChart.getOption();
        option.series[0].data[params.dataIndex].x = params.event.offsetX;
        option.series[0].data[params.dataIndex].y = params.event.offsetY;
        option.series[0].data[params.dataIndex].fixed = true;
        myChart.setOption(option);
      });
      window.addEventListener("resize", function () {
        myChart.resize();
      });
    },
    handleAnalysis(index, row) {
      axios.get("ana/exam_analysis/?exam_id=" + row.id).then(
          res => {
            this.data = res.data.rules
            this.title = row.name + ' 知识点相关度数据分析图'
            this.anaFormVisible = true

            setTimeout(() => {
              this.data2Graph();
            }, 1);
          }
      )
    },
    handleUpdate(index, row) {
      console.log(row)
      axios.put('ana/exam/' + row.id + '/').then(
          res => {
            this.getFormValue(this.currentExamPage)
          }
      )
    },
  },
  created() {
    this.getFormValue(1)
  }
}
</script>

<style scoped>

</style>