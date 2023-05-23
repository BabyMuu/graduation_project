<script setup>
import {Timer} from '@element-plus/icons-vue'
import {Phone} from '@element-plus/icons-vue'
import {RefreshRight} from '@element-plus/icons-vue'
import {Search} from '@element-plus/icons-vue'
</script>

<template>
  <br>
  <!-- 表格头开始 -->
  <div style="margin-left: 10%">
    <el-button type="primary" :icon="RefreshRight" circle
               @click="this.getFormValue(this.currentUserPage); "/>&nbsp;
    <el-button type="primary" @click="newOrder">新增订单</el-button>&nbsp;
    <el-button type="danger" @click="this.createFormVisible=true">批量删除</el-button>

    <div style="float: right; display: inline; margin-right: 13%">
      <el-input
          v-model="searchBy"
          placeholder="Please input username"
      >
        <template #append>
          <el-button :icon="Search" @click=""/>
        </template>
      </el-input>
    </div>
  </div>
  <br>
  <!-- 表格头结束 -->
  <!-- 表格开始 -->
  <el-table :data="orders"
            :header-cell-style="{'text-align':'center'}"
            :cell-style="{'text-align':'center'}"
            border style="width: 80%; margin-left: 10%;"
            @selection-change="UserSelectionChange"
  >
    <el-table-column type="selection" width="55"/>
    <el-table-column label="#" type="index" width="80"/>
    <el-table-column label="支付方式">
      <template #default="scope">
        {{ scope.row.payment }}
      </template>
    </el-table-column>

    <el-table-column label="商品数量">
      <template #default="scope">
        <div>
          <span>{{ scope.row.count }}</span>
        </div>
      </template>
    </el-table-column>

    <el-table-column label="商品名" width="140">
      <template #default="scope">
        <div>
          <span>{{ scope.row.name }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="购买者">
      <template #default="scope">
        <div>
          <span>{{ scope.row.username }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="支付金额">
      <template #default="scope">
        <div>
          <span>{{ scope.row.payPrice }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="支付时间" width="180">
      <template #default="scope">
        <div>
          <span>{{ scope.row.payTime }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="创建时间" width="180">
      <template #default="scope">
        <div>
          <span>{{ scope.row.createTime }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="修改时间" width="180">
      <template #default="scope">
        <div>
          <span>{{ scope.row.updatedTime }}</span>
        </div>
      </template>
    </el-table-column>


    <el-table-column label="操作" width="180">
      <template #default="scope">

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
      :total="orderTotal"
      @current-change="getFormValue"
  />
  <!-- 分页结束 -->
  <!-- 新建表单开始 -->
  <el-dialog v-model="createFormVisible" title="新增订单" show-close style="margin-top: 10%">
    <el-form :model="createForm" label-width="120px">
      <el-form-item label="用户ID" prop="userId">
        <el-input v-model="createForm.userId"/>
      </el-form-item>
      <el-form-item label="商品ID" prop="goodId">
        <el-input v-model="createForm.goodId"/>
      </el-form-item>
      <el-form-item label="支付方式" prop="payment">
        <el-input v-model="createForm.payment"/>
      </el-form-item>
      <el-form-item label="购买商品数量" prop="count">
        <el-input v-model="createForm.count"/>
      </el-form-item>
      <el-form-item label="支付金额" prop="payPrice">
        <el-input v-model="createForm.payPrice"/>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="createForm.info" type="textarea"/>
      </el-form-item>
      <div style="height: 30px">
        <el-button style="float: right; margin-right: 10%">Cancel</el-button>
        <el-button style="float: right; margin-right: 5%" type="primary" @click="createSubmit">Submit</el-button>
      </div>

    </el-form>
  </el-dialog>
  <!-- 新建表单结束 -->

</template>

<script>
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  name: "OrderView",
  data() {
    return {
      searchBy: "",
      // 分页
      pageSize: 15,
      orderTotal: 1000,
      currentUserPage: 1,
      // 修改
      editFormVisible: false,
      // 修改确认(用户名是否重复)
      editSubmitDisable: false,
      editForm: {},
      // 新增
      createFormVisible: false,
      createForm: {},
      defaultCreateForm: {
        payment: '',
        count: '',
        payTime: '',
        goodId: '',
        userId: '',
        payPrice: '',
      },
      role: {0: "管理员", 1: "普通用户"},
      orders: [
        {
          id: 1,
          is_deleted: "sd",
          createTime: 'sd',
          updatedTime: 'sd',
          payment: 'sd',
          count: 'sd',
          payTime: 'd',
          name: 'd',
          username: 'd',
          payPrice: 'd',

        },
      ],
    }
  },
  methods: {
    UserSelectionChange() {
    },
    // 添加用户
    newOrder() {
      this.createForm.payment = this.defaultCreateForm.payment;
      this.createForm.count = this.defaultCreateForm.count;
      this.createForm.payTime = this.defaultCreateForm.payTime;
      this.createForm.goodId = this.defaultCreateForm.goodId;
      this.createForm.userId = this.defaultCreateForm.userId;
      this.createForm.payPrice = this.defaultCreateForm.payPrice;
      this.createFormVisible = true
    },
    createSubmit(config) {
      axios.post("orders", this.createForm, {"contentType": "application/json", "dataType": "json"}).then(
          res => {
            ElMessage.success("新增订单成功")
            this.createFormVisible = false
            this.getFormValue(this.currentUserPage)
          }
      ).catch(
          err => {
            ElMessage.error("新增用户失败! " + err.response.data.msg)
          }
      )
    },
    // 删除用户
    handleDelete(row, data) {
      axios.delete("orders", {
        params: {
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
    // 获取所有用户数据  分页获取
    getFormValue(pageNum) {
      axios.get("orders/?page=" + pageNum, {}
      ).then(response => {
        this.orders = response.data.data.orders
        this.orderTotal = response.data.data.count
      })
    },
  },
  created() {
    this.getFormValue(1)
    axios.get("roles").then(
        res => {
          this.roles = res.data.data
          console.log(this.roles)
        }
    ).catch(
        err => {
          ElMessage.error("权限映射请求失败!", err.response.data.msg)
        }
    )
  }
}
</script>

<style scoped>

</style>