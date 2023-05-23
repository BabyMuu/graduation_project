<template>
  <div class="about">
    <h1>This is an about page</h1>
    <div id='charts' style="width: 800px; height: 800px">
      hello world
    </div>
    <button @click="change">hell</button>
  </div>
</template>
<script>
export default {
  name: 'about',
  data() {
    return {
      data: [5, 20, 36, 10, 10, 20]
    }
  },
  mounted() {
    this.draw1()
  },
  methods: {
    change(){
      this.data = [20, 20, 36, 10, 10, 20]
      this.draw1()
    },
    draw1() {
      // 基于准备好的dom，初始化echarts实例，注意id不要写错
      let myChart = this.$echarts.init(document.getElementById('charts'))
      // 绘制图表
      let option = {
        title: {text: 'Echarts'},
        tooltip: {},
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [{
          name: '销量',
          type: 'bar',
          data: this.data
        }]
      }
      option && myChart.setOption(option)
      window.addEventListener("resize", function () {
        myChart.resize();
      });
    },
  },
}
</script>
<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
