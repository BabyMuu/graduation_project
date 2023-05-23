function draw() {
    var text = [['一次函数', '二次函数', 0.64], ['二次函数', '一次函数', 0.78], ['一次函数', '四边形', 0.73], ['四边形', '一次函数', 0.89], ['一次函数', '实数', 0.82], ['实数', '一次函数', 0.82], ['一次函数', '概率', 0.64], ['概率', '一次函数', 0.7], ['一次函数', '轴对称', 0.82], ['轴对称', '一次函数', 0.9], ['不等式', '实数', 0.88], ['实数', '不等式', 0.64], ['二次函数', '四边形', 0.78], ['四边形', '二次函数', 0.78], ['二次函数', '实数', 0.89], ['实数', '二次函数', 0.73], ['四边形', '实数', 0.89], ['实数', '四边形', 0.73], ['四边形', '轴对称', 0.78], ['轴对称', '四边形', 0.7], ['概率', '实数', 0.7], ['实数', '概率', 0.64], ['轴对称', '实数', 0.9], ['实数', '轴对称', 0.82], ['概率', '轴对称', 0.7], ['轴对称', '概率', 0.7], ['二次函数', '分式', 0.78], ['分式', '二次函数', 1.0], ['四边形-一次函数', '实数', 0.88], ['实数-一次函数', '四边形', 0.78], ['实数-四边形', '一次函数', 0.88], ['四边形-一次函数', '实数', 0.88], ['实数-一次函数', '四边形', 0.78], ['实数-四边形', '一次函数', 0.88], ['轴对称-一次函数', '实数', 0.89], ['实数-一次函数', '轴对称', 0.89], ['实数-轴对称', '一次函数', 0.89], ['轴对称-一次函数', '实数', 0.89], ['实数-一次函数', '轴对称', 0.89], ['实数-轴对称', '一次函数', 0.89], ['轴对称-四边形', '实数', 1.0], ['实数-四边形', '轴对称', 0.88], ['实数-轴对称', '四边形', 0.78], ['轴对称-四边形', '实数', 1.0], ['实数-四边形', '轴对称', 0.88], ['实数-轴对称', '四边形', 0.78]];
    var data = eval(text);
    var graph = data2Graph(data);
    drawGraph(graph);
}

function data2Graph(data) {
    var graph = {}
    var vertices = {}
    var links = [];
    for (var i = 0; i < data.length; i++) {
        var s = String(data[i][0]);
        var t = String(data[i][1]);
        var v = data[i][2];
        vertices[s] = s;
        vertices[t] = t;
        links.push({'source': s, 'target': t, 'value': v});
    }
    var nodes = [];
    $.each(vertices, function (k, v) {
        nodes.push({'name': v, 'value': v});
    });
    graph['links'] = links;
    graph['data'] = nodes;
    return graph;
}

function drawGraph(graph) {
    var myChart = echarts.init(document.getElementById("echarts-main"));
    var option = {
        tooltip: {},
        series: [
            {
                type: 'graph',
                layout: 'force',
                symbolSize: 60,

                edgeSymbol: ['circle', 'arrow'],
                data: graph.data,
                links: graph.links,
                roam: true,
                label: {
                    show: true,
                    normal: {
                        formatter: function (e) {
                            return e['data']['value'];
                        },
                    },

                },
                edgeLabel: {
                    normal: {
                        show: true,
                        position: 'middle',
                    }
                },
                force: {
                    repulsion: 6000,
                    edgeLength: 200
                }
            }
        ]
    };
    myChart.setOption(option);
}

function initInvisibleGraphic() {
    // Add shadow circles (which is not visible) to enable drag.
    myChart.setOption({
        graphic: echarts.util.map(option.series[0].data, function (item, dataIndex) {
            //使用图形元素组件在节点上划出一个隐形的图形覆盖住节点
            var tmpPos = myChart.convertToPixel({'seriesIndex': 0}, [item.x, item.y]);
            return {
                type: 'circle',
                id: dataIndex,
                position: tmpPos,
                shape: {
                    cx: 0,
                    cy: 0,
                    r: 20
                },
                // silent:true,
                invisible: true,
                draggable: true,
                ondrag: echarts.util.curry(onPointDragging, dataIndex),
                z: 100              //使图层在最高层
            };
        })
    });
    window.addEventListener('resize', updatePosition);
    myChart.on('dataZoom', updatePosition);
}

myChart.on('graphRoam', updatePosition);

function updatePosition() {    //更新节点定位的函数
    myChart.setOption({
        graphic: echarts.util.map(option.series[0].data, function (item, dataIndex) {
            var tmpPos = myChart.convertToPixel({'seriesIndex': 0}, [item.x, item.y]);
            return {
                position: tmpPos
            };
        })
    });

}

function onPointDragging(dataIndex) {      //节点上图层拖拽执行的函数
    var tmpPos = myChart.convertFromPixel({'seriesIndex': 0}, this.position);
    option.series[0].data[dataIndex].x = tmpPos[0];
    option.series[0].data[dataIndex].y = tmpPos[1];
    myChart.setOption(option);
    updatePosition();
}
