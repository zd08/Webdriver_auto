# encoding:utf-8
import os
import time
from string import Template
class Test_result(object):
    def __init__(self,**kwargs):
        self.parentDirPath = os.path.dirname(os.path.abspath(__file__))
        self.time = str(time.strftime('%Y_%m_%d_%M_%I_%S' , time.localtime()))+'.html'
        self.path = os.path.join(self.parentDirPath,'test_report',self.time)
        self.start_time=kwargs['start_time']
        self.count_time = kwargs['count_time']
        self.success=kwargs['success']
        self.fail_count = kwargs['fail_count']
        self.table = kwargs['table']
        self.result()
        self.file_build()

    def result(self):
        self.held = '''   
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <!-- import CSS -->
        <!-- 引入样式 -->
        <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
        <!-- 引入组件库 -->
        <script src="echarts.min.js"></script>
        <!-- import Vue before Element -->
        <script src="https://unpkg.com/vue/dist/vue.js"></script>
        <!-- import JavaScript -->
        <script src="https://unpkg.com/element-ui/lib/index.js"></script>
        </head>'''

        self.body =Template( '''
            <body>
        <div id="app" style="background-color:rgb(205 213 224)">
        <el-row>
        <el-col :span="24"><div class="grid-content" style="margin:0 auto;text-aligin:center;">
        <h2 align="center">自动化测试报告</h2>
        </div></el-col>
        </el-row>
        <el-row>
        <el-col :span="8"><div class="grid-content">
        <h5>&nbsp&nbsp&nbsp&nbsp执行时间：${start_time}</h5>
        <h5>&nbsp&nbsp&nbsp&nbsp运行时间：${count_time}</h5>
        <h5>用例通过数：${success}</h5>
        </div>
        </el-col>
        
        <el-col :span="16"><div class="grid-content">
        <div id="main" style="width: 400px;height:200px;"></div>
        </div></el-col></el-row>
        
        <el-row><el-col :span="24"><div>
        <template>
        <el-table
        :data="tableData"
        :header-cell-style="tableHeaderColor"
        height="370"
        border  
        :cell-style="cellStyle"
        style="width: 100%">
        <el-table-column
          prop="test_case"
          label="测试用例"
          width="400"
          align="center">
        </el-table-column>
        <el-table-column
          prop="count"
          label="总数"
          align="center">
        </el-table-column>
        <el-table-column
          prop="pass"
          label="通过"
          align="center">
        </el-table-column>
        <el-table-column
          prop="fail"
          label="失败"
          align="center">
        </el-table-column>
        <el-table-column
          prop="error"
          label="错误"
          align="center">
        </el-table-column>
        <el-table-column
          prop="view"
          label="视图"
          align="center">
        </el-table-column>
        <el-table-column
          prop="error_view"
          label="错误截图"
          align="center">
        </el-table-column>
        </el-table>
        </template>
        
        </div></el-col>
        </el-row>
        </div>
        <style>
        .el-row {
        margin-bottom: 20px;
        &:last-child {
          margin-bottom: 0;
        }
        }
        .el-col {
        border-radius: 4px;
        }
        .bg-purple-dark {
        background: #99a9bf;
        }
        .bg-purple {
        background: #d3dce6;
        }
        .bg-purple-light {
        background: #e5e9f2;
        }
        .grid-content {
        border-radius: 4px;
        min-height: 36px;
        }
        </style>
        
        </body>
        <style lang="less" scoped>
        #myChart{
        width: 100%;
        }
        </style>
            ''').safe_substitute(start_time=self.start_time,count_time=self.count_time,success=self.success)
        self.table_result=''
        for i in self.table:
            if i[2] == 'pass':
                self.table_result +=Template('''{
                            test_case:' ${table0}',
                            count: '${table1}',
                            pass: '${table2}',
                            fail:"",
                            error:'',
                            view:'',
                            error_view:'',
                            },''').safe_substitute(table0=i[0],table1=i[1],table2='pass')
            else:
                self.table_result += Template('''{
                                            test_case: '${table0}',
                                            count: '${table1}',
                                            pass: "",
                                            fail:'${table2}',
                                            error:'',
                                            view:'',
                                            error_view:'',
                                            },''').safe_substitute(table0=i[0], table1=i[1], table2='fail')

        self.table = Template('''
        <script>
        new Vue({
        el: '#app',
        data: function() {
        return { visible: false,
        tableData: [${result_table}] 
        }
        },
        created() {},
        methods: {
    // 修改table tr行的背景色
    tableRowStyle({ row, rowIndex }) {
      return 'background-color: pink'
    },
    // 修改table header的背景色
    tableHeaderColor({ row, column, rowIndex, columnIndex }) {
      if (rowIndex === 0) {
        return 'background-color: lightblue;color: #fff;font-weight: 500;text-align:center'
      }
    },
    cellStyle(row, column, rowIndex, columnIndex){//根据报警级别显示颜色
        // console.log(row);
        console.log(row.column.label);
        if (row.column.label==="通过" && row.row.pass==="pass"){
          return 'color:green'
        }else if(row.column.label==="失败" && row.row.fail==="pass" ){
          return 'color:red'
        }
      },}

        })
        
        </script>
        ''').safe_substitute(result_table=self.table_result)
        self.view =Template('''
        <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.querySelector('#main'));
        var option = {
        //设置
        tooltip:{
        trigger:'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        //对图例组件的不同系列进行标记说明
        legend:{
        orient:'vertical',  //设置图例列表的布局朝向
        left:'left',
        data:['成功数量','失败数量']
        
        },
        //系列列表
        series:[
        //系列1
        {
        name:'测试用例',
        type:'pie',    //数据统计图的类型
        //放置要展示的数据
        data:[
        {value:${success},name:'成功数量',itemStyle:{color:"#00CC00"}},
        {value:${fail_count},name:'失败数量',itemStyle:{color:"red"}},
        ]
        }
        ]
        }
        
        myChart.setOption(option);
        </script>
        </html>
        ''').safe_substitute(success = self.success,fail_count=self.fail_count)

    def file_build(self):
        with open(self.path,'a',encoding="utf-8") as f:
            f.write(self.held+self.body+self.table+self.view)


# a=Test_result()
# a.result()
# a.file_build()
