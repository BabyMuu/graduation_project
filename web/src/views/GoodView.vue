<script setup>
import {Timer} from '@element-plus/icons-vue'
import {Phone} from '@element-plus/icons-vue'
import {RefreshRight} from '@element-plus/icons-vue'
import {Search} from '@element-plus/icons-vue'
</script>
<template>
  <br>
  <!-- 表格头开始 -->
  <div style="margin-left: 3%">
    <el-button type="primary" :icon="RefreshRight" circle
               @click="this.getFormValue(this.currentUserPage); "/>&nbsp;
    <el-button type="primary" @click="newGood">新增商品</el-button>&nbsp;
    <el-button type="danger" @click="this.createFormVisible=true">批量删除</el-button>
    <div style="float: right; display: inline; margin-right: 13%">
      <el-input
          v-model="searchBy"
          placeholder="         请输入商品名称"
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
  <el-table :data="goods"
            :header-cell-style="{'text-align':'center'}"
            :cell-style="{'text-align':'center'}"
            border style="width: 90%; margin-left: 3%;"
            @selection-change="UserSelectionChange"
  >
    <el-table-column type="selection" width="55"/>
    <el-table-column label="#" type="index" width="80"/>
    <el-table-column label="商品分类" width="180">
      <template #default="scope">
        <div>
          <span>{{ scope.row.sort }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="商品名" width="180">
      <template #default="scope">
        <el-popover
            placement="top-start"
            trigger="hover"
            width="100"
        >
          <img :src="scope.row.name + '.jpg'" style="width: 100px; height: 100px"/>
          <template #reference>
            <el-tag>{{ scope.row.name }}</el-tag>
          </template>
        </el-popover>
      </template>
    </el-table-column>
    <el-table-column label="商品单价">
      <template #default="scope">
        <div>
          <span>{{ scope.row.price }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="库存数量">
      <template #default="scope">
        <div>
          <span>{{ scope.row.amount }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="状态" width="113">
      <template #default="scope">
        <div>
          <el-tag type="success" v-if="scope.show">上架中</el-tag>
          <el-tag type="danger" v-if="!scope.show">未上架</el-tag>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="更新时间" width="205">
      <template #default="scope">
        <div>
          <el-icon>
            <phone/>
          </el-icon>
          <span style="margin-left: 10px">{{ scope.row.updatedTime }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="修改时间" width="205">
      <template #default="scope">
        <div>
          <el-icon>
            <timer/>
          </el-icon>
          <span style="margin-left: 10px">{{ scope.row.createTime }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="250">
      <template #default="scope">
        <el-button size="small" :type=" scope.show ? 'danger' : 'success' "
                   @click="changeGoodStatus(scope.$index, scope.row)"
        >{{ scope.show ? "下架" : "上架" }}
        </el-button>
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
        >Edit
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
      :total="userTotal"
      @current-change="getFormValue"
  />
  <!-- 分页结束 -->
  <!-- 编辑表单开始 -->
  <el-dialog v-model="editFormVisible" title="用户编辑">
    <el-form :model="editForm" label-width="120px">
      <el-form-item label="Username" prop="username">
        <el-input v-model="editForm.username" style="width: 70%"/>
        <span style="width: 10%"></span>
        <el-button style="width: 20%" @click="checkUser">检查用户名是否存在</el-button>
      </el-form-item>
      <el-form-item label="phone" prop="phoneNum">
        <el-input v-model="editForm.phoneNum"/>
      </el-form-item>
      <el-form-item label="password" prop="password">
        <el-input v-model="editForm.password"/>
      </el-form-item>
      <el-form-item label="Create time" prop="createTime">
        <el-col :span="11">
          <el-date-picker disabled
                          v-model="editForm.createTime"
                          type="date"
                          placeholder="Pick a date"
                          style="width: 100%"
          />
        </el-col>
      </el-form-item>
      <el-form-item label="权限" prop="role">
        <el-radio-group v-model="editForm.roleId ">
          <el-radio :label="0">管理员</el-radio>
          <el-radio :label="1">普通用户</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="editForm.desc" type="textarea"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="editSubmit" :disabled="editSubmitAble">Submit</el-button>
        <el-button>Cancel</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <!-- 编辑表单结束 -->
  <!-- 新建表单开始 -->
  <el-dialog v-model="createFormVisible" title="新增用户" show-close style="margin-top: 10%">
    <el-form :model="createForm" label-width="120px">
      <el-form-item label="商品分类" prop="sort">
        <el-input v-model="createForm.sort"/>
      </el-form-item>
      <el-form-item label="商品名称" prop="name">
        <el-input v-model="createForm.name"/>
      </el-form-item>
      <el-form-item label="商品简介" prop="info">
        <el-input v-model="createForm.info"/>
      </el-form-item>
      <el-form-item label="商品单价" prop="price">
        <el-input-number v-model="createForm.price" :min="1" :max="1000000000" style="width: 50%"/>
      </el-form-item>
      <el-form-item label="库存数量" prop="amount">
        <el-input-number v-model="createForm.amount" :min="1" :max="100000" style="width: 50%"/>
      </el-form-item>
      <el-form-item label="是否上架" prop="isShow">
        <el-radio-group v-model="createForm.isShow">
          <el-radio :label="true">是</el-radio>
          <el-radio :label="false">否</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="createForm.desc" type="textarea"/>
      </el-form-item>
      <div style="height: 30px">
        <el-button style="float: right; margin-right: 10%" @click="createFormVisible=false">Cancel</el-button>
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
  name: "GoodView",
  data() {
    return {
      searchBy: "",
      // 分页
      pageSize: 15,
      userTotal: 1000,
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
        amount: 1,
        icon: "",
        info: "",
        name: "",
        price: 0,
        isShow: true,
        sort: "",
      },
      role: {0: "管理员", 1: "普通用户"},
      goods: [
        {
          amount: 1,
          createTime: "2022-09-06",
          deleted: false,
          icon: null,
          id: 1,
          info: "商品",
          name: "梳子",
          price: 1,
          show: true,
          sort: "日用品",
          updatedTime: "2022-09-06",
        },
      ],
    }
  },
  methods: {
    UserSelectionChange() {
    },
    // 添加用户
    newGood() {
      this.createForm.username = this.defaultCreateForm.username;
      this.createForm.password = this.defaultCreateForm.password;
      this.createForm.phoneNum = this.defaultCreateForm.phoneNum;
      this.createForm.roleId = this.defaultCreateForm.roleId;
      this.createFormVisible = true
    },
    createSubmit(config) {
      console.log(this.createForm)
      axios.post("goods", this.createForm, {"contentType": "application/json", "dataType": "json"}).then(
          res => {
            ElMessage.success("新增商品:" + this.createForm.name + "成功")
            this.createFormVisible = false
          }
      ).catch(
          err => {
            ElMessage.error("新增商品失败! " + err.response.data.msg)
          }
      )
    },
    // 删除
    handleDelete(row, data) {
      axios.delete("users", {
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
    // 修改商品状态
    changeGoodStatus(index, row) {
      axios.put("goods/shelf", {
        id: row.id,
        isShow: !row.show
      },).then(
          res => {
            ElMessage.success("商品:", row.name, "状态切换成功")
            this.getFormValue(this.currentUserPage)
          }
      ).catch(
          err => {
            ElMessage.error("请求失败! " + err.response.data.msg)
          }
      )
      this.getFormValue(this.currentUserPage)
    },
    handleEdit(index, row) {
      this.editForm.id = row.id
      this.editForm.baseUsername = row.username
      this.editForm.password = row.password
      this.editForm.phoneNum = row.phoneNum
      this.editForm.roleId = row.roleId
      this.editForm.username = row.username
      this.editFormVisible = true
    },
    editSubmit() {
      if (this.editForm.username.trim() !== this.editForm.baseUsername.trim() && this.checkUser()) {
        return
      }
      axios.put("users", this.editForm
      ).then(
          res => {
            ElMessage.success("修改成功")
            this.editFormVisible = false
            this.editForm = {}
          }
      ).catch(
          err => {
            ElMessage.success("修改失败!", err.data.msg)
          }
      )

    },
    // 获取所有用户数据  分页获取
    getFormValue(pageNum) {
      axios.get("goods/?page=" + pageNum
      ).then(response => {
        this.goods = response.data.data.goods
        this.userTotal = response.data.data.count
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