<script setup>
import {ref} from 'vue'
import {ElForm} from 'element-plus'
import {ElMessage} from 'element-plus'
</script>

<template>
  <div class="default-main">
    <el-row :gutter="30">
      <el-col class="lg-mb-20" :xs="24" :sm="24" :md="24" :lg="10">
        <div class="admin-info" style="background-color: white; margin-top: 10%; margin-left: 5%">
          <el-upload
              class="avatar-uploader"
              action="images"
              :show-file-list="false"
              :auto-upload="true"
              :on-success="handleAvatarSuccess"
              accept="image/gif, image/jpg, image/jpeg, image/bmp, image/png, image/webp"
          >
            <el-image :src="userInfo.icon" class="avatar">
              <template #error>
                <div class="image-slot">
                  <Icon size="30" color="#c0c4cc" name="el-icon-Picture"/>
                </div>
              </template>
            </el-image>
          </el-upload>
          <div class="admin-info-base">
            <div class="admin-nickname">{{ userInfo.username }}</div>
            <div class="admin-other">
              <div>{{ '上次登录时间: ' }} {{ userInfo.updateTime }}</div>
            </div>
          </div>
          <div class="admin-info-form">
            <el-form
                ref="userInfo"
                v-model="userInfo"
                label-position="top"
            >
              <el-form-item label="用户名">
                <el-input disabled v-model="userInfo.username"></el-input>
              </el-form-item>
              <el-form-item label="权限" prop="permission">
                <el-input disabled
                          v-model="userInfo.permission"
                ></el-input>
              </el-form-item>
              <el-form-item label="账号创建时间" prop="createTime">
                <el-input disabled
                          v-model="userInfo.createTime"></el-input>
              </el-form-item>
              <el-form-item label="手机号码" prop="mobile">
                <el-input
                    placeholder="Please input field"
                    v-model="userInfo.phone"
                ></el-input>
              </el-form-item>

              <el-form-item label="密码" prop="password">
                <el-input
                    type="password"
                    placeholder="请输入需要更改的密码, 如不需要请留空"
                    v-model="userInfo.password"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit">{{
                    '确认修改'
                  }}
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :md="24" :lg="10">
        <el-card header="历史订单" shadow="never" style="background-color: white; margin-top: 10%; margin-left: 5%">
          <el-timeline>
            <el-timeline-item v-for="(item, idx) in orders" :key="idx" size="large"
                              :timestamp="item.createTime">
              {{ item.name }}
            </el-timeline-item>
          </el-timeline>
          <el-pagination
              :currentPage="currentPage"
              :page-size="12"
              background
              layout="prev, next, jumper"
              :total="orderTotal"
              @current-change="onLogCurrentChange"
          ></el-pagination>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>


<script>
import {defineComponent, ref} from 'vue'
import axios from "axios";
import {ElMessage} from "element-plus";

export default defineComponent({
  name: 'routine/adminInfo',
  data() {
    return {
      userInfo: {
        username: "admin",
        permission: "管理员",
        createTime: "2019-07-11 22:11:20",
        phone: "15624246767",
        password: "",
        icon: "",
        updateTime: "2019-07-11 22:11:20"
      },
      orders: [
        {
          createTime: '2019-01-23 12:35:20',
          name: "牛肉"
        },
      ],
      orderTotal: ref(100),
      currentPage: 1,
    }
  },
  methods: {
    getOrderHistory() {
      axios.get("orderHistory", {
        page: this.currentPage
      }).then(
          res => {
            this.orders = res.data.data.orders
            this.orderTotal = res.data.data.count
          }
      )
    },
    onLogCurrentChange() {
      this.getOrderHistory()
    },
    onSubmit() {
      if (this.userInfo.password !== "") {
        axios.post("users/password", {
          password: this.userInfo.password
        }).then(
        ).catch(
            ElMessage.success("密码修改失败")
        )
      }
      axios.post("account", {
        phoneNum: this.userInfo.phone
      }).then(
          res => {
            ElMessage.success("修改信息成功")
          }
      ).catch(
          err => {
            ElMessage.error("修改信息失败")
          }
      )
      this.getUserInfo()
    },
    handleAvatarSuccess(response, uploadFile) {
      this.getUserInfo()
    },
    getUserInfo() {
      axios.get("account").then(
          res => {
            this.userInfo = res.data.data.userInfo
          }
      )
    }
  },
  created() {
    this.getUserInfo()
    this.getOrderHistory()
  }
})
</script>

<style scoped lang="scss">
.admin-info {
  background-color: var(--ba-bg-color-overlay);
  border-radius: var(--el-border-radius-base);
  border-top: 3px solid #409eff;

  .avatar-uploader {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    margin: 60px auto 10px auto;
    border-radius: 50%;
    box-shadow: var(--el-box-shadow-light);
    border: 1px dashed var(--el-border-color);
    cursor: pointer;
    overflow: hidden;
    width: 110px;
    height: 110px;
  }

  .avatar-uploader:hover {
    border-color: var(--el-color-primary);
  }

  .avatar {
    width: 110px;
    height: 110px;
    display: block;
  }

  .image-slot {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }

  .admin-info-base {
    .admin-nickname {
      font-size: 22px;
      color: var(--el-text-color-primary);
      text-align: center;
      padding: 8px 0;
    }

    .admin-other {
      color: var(--el-text-color-regular);
      font-size: 14px;
      text-align: center;
      line-height: 20px;
    }
  }

  .admin-info-form {
    padding: 30px;
  }
}

.el-card :deep(.el-timeline-item__icon) {
  font-size: 10px;
}

@media screen and (max-width: 1200px) {
  .lg-mb-20 {
    margin-bottom: 20px;
  }
}
</style>
