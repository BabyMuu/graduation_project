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
  <el-table :data="users"
            :header-cell-style="{'text-align':'center'}"
            :cell-style="{'text-align':'center'}"
            border style="width: 80%; margin-left: 10%;"
            @selection-change="UserSelectionChange"
  >
    <el-table-column type="selection" width="55"/>
    <el-table-column label="#" type="index" width="80"/>

    <el-table-column label="姓名" width="180">
      <template #default="scope">
        <el-tag>{{ scope.row.name }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column label="班级编号" width="180">
      <template #default="scope">
        <div>
          <span>{{ scope.row.class_id }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="Operations">
      <template #default="scope">
        <el-button size="small" @click="handleCheck(scope.$index, scope.row)"
        >查看考试成绩
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
      <el-form-item label="用户名" prop="username">
        <el-input v-model="createForm.username"/>
      </el-form-item>
      <el-form-item label="密码" prop="Password">
        <el-input v-model="createForm.Password"/>
      </el-form-item>
      <el-form-item label="手机号" prop="phoneNum">
        <el-input v-model="createForm.phoneNum"/>
      </el-form-item>
      <el-form-item label="权限" prop="role">
        <el-radio-group v-model="createForm.roleId">
          <el-radio :label="0">管理员</el-radio>
          <el-radio :label="1">普通用户</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="picture-upload" prop="picLoad">
        <el-upload :file-list="pictureupload109740FileList" :headers="pictureupload109740UploadHeaders"
                   :data="pictureupload109740UploadData" list-type="picture-card" show-file-list :limit="3">
          <template
              #default><i class="el-icon-plus"></i></template>
        </el-upload>
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
        username: '',
        password: '',
        phoneNum: '',
        roleId: 1,
        picLoad: ""
      },
      role: {0: "管理员", 1: "普通用户"},
      users: [
        {
          id: 1,
          name: 'Tom',
          username: 'mark',
          createDate: '2016-05-03',
          phone: '12345678901',
          permissions: '管理员',
        },
        {
          id: 2,
          createDate: '2016-05-02',
          phone: '12345678901',
          permissions: '管理员',
          name: 'Tom',
          username: 'mark',
        },
        {
          id: 3,
          createDate: '2016-05-04',
          phone: '12345678901',
          permissions: '管理员',
          name: 'Tom',
          username: 'mark',
        },
      ],
    }
  },
  methods: {
    UserSelectionChange() {
    },
    // 添加用户
    newUser() {
      this.createForm.username = this.defaultCreateForm.username;
      this.createForm.password = this.defaultCreateForm.password;
      this.createForm.phoneNum = this.defaultCreateForm.phoneNum;
      this.createForm.roleId = this.defaultCreateForm.roleId;
      this.createForm.picLoad = this.defaultCreateForm.picLoad;
      this.createFormVisible = true
    },
    createSubmit(config) {
      console.log(this.createForm)
      axios.post("users", this.createForm, {"contentType": "application/json", "dataType": "json"}).then(
          res => {
            ElMessage.success("新增用户:" + this.createForm.username + "成功")
            this.createFormVisible = false
          }
      ).catch(
          err => {
            ElMessage.error("新增用户失败! " + err.response.data.msg)
          }
      )
    },
    // 删除用户
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
    // 修改用户
    handleCheck(index, row) {
      this.$router.push({
        path: '/score',
        query: {
          id: row.user_id
        }
      })
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
    checkUser() {
      let flag = false
      axios.get("usernames", {
        params: {
          username: this.editForm.username
        }
      }).then(
          res => {
            flag = res.data.data.userHasExist
            if (flag) {
              ElMessage.error("用户名已存在!")
            } else {
              ElMessage.success("您可以使用此用户名")
            }
          }
      ).catch(
          err => {
            this.editSubmitDisable = true
          }
      )
      return flag
    },
    // 获取所有用户数据  分页获取
    getFormValue(pageNum) {
      axios.get("user/stu/?page=" + pageNum, {}
      ).then(response => {
        this.users = response.data.results
        this.userTotal = response.data.count
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