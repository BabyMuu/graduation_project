<template>
  <div class="login">
    <div class="mylogin" align="center">
      <h4>{{ type }}</h4>
      <el-form
          :model="loginForm"
          :rules="loginRules"
          ref="loginForm"
          label-width="0px"
      >
        <el-form-item label="" prop="account" style="margin-top: 10px">
          <el-row>
            <el-col :span="2">
              <span class="el-icon-s-custom"></span>
            </el-col>
            <el-col :span="22">
              <el-input
                  class="inps"
                  placeholder="账号"
                  v-model="loginForm.account"
              >
              </el-input>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="" prop="passWord">
          <el-row>
            <el-col :span="2">
              <span class="el-icon-lock"></span>
            </el-col>
            <el-col :span="22">
              <el-input
                  class="inps"
                  type="password"
                  placeholder="密码"
                  v-model="loginForm.passWord"
              ></el-input>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="" prop="classId" v-if="type ==='注册'">
          <el-row>
            <el-col :span="2">
              <span class="el-icon-lock"></span>
            </el-col>
            <el-col :span="22">
              <el-input
                  class="inps"
                  placeholder="班级号"
                  v-model="loginForm.classId"
              ></el-input>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item style="margin-top: 40px; margin-left: 18px">
          <el-button type="primary" round class="submitBtn" @click="submitForm"
          >{{ type }}
          </el-button>
        </el-form-item>
        <el-form-item style="margin-top: 20px; margin-left: 18px">
          <el-button type="primary" round class="submitBtn" @click="changeType">
            {{ type === '登录' ? '注册新账号' : "登录账号" }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>


<script>
import {mapMutations} from "vuex";
import {ElMessage} from "element-plus";
import axios from "axios";

export default {
  name: "LoginView",
  data: function () {
    return {
      type: "登录",
      loginForm: {
        account: "",
        passWord: "",
        classId: "",
      },
      loginRules: {
        account: [{required: true, message: "请输入账号", trigger: "blur"}],
        passWord: [{required: true, message: "请输入密码", trigger: "blur"}],
      },
    };
  },

  methods: {
    ...mapMutations(["changeLogin"]),
    changeType() {
      if (this.type === "登录") {
        this.type = '注册'
      } else {
        this.type = '登录'
      }
      this.loginForm.account = ""
      this.loginForm.passWord = ""
    },
    submitForm() {
      const userAccount = this.loginForm.account;
      const userPassword = this.loginForm.passWord;
      if (!userAccount) {
        return this.$message({
          type: "error",
          message: "账号不能为空！",
        });
      }
      if (!userPassword) {
        return this.$message({
          type: "error",
          message: "密码不能为空！",
        });
      }
      if (this.type === "登录") {
        axios.post("user/login/", {
          username: userAccount,
          password: userPassword
        }).then(
            res => {
              let name = res.data['']
              localStorage.setItem("username", userAccount)
              ElMessage.success("登录成功, 欢迎您, " + userAccount)
              this.$router.push('index')
            }
        ).catch(
            err => {
              ElMessage.error("登录失败! ", err.response.data.msg)
            }
        )
      } else {
        axios.post(
            "user/users/", {
              username: this.loginForm.account,
              classes: this.loginForm.classId,
              password: this.loginForm.passWord,
              name: this.loginForm.account,
              types: 1
            }
        ).then(
            res => {
              ElMessage.success("注册成功")
              this.loginForm.account = ""
              this.loginForm.passWord = ""
              this.loginForm.classId = ""
              this.type = "登录"
            }
        ).catch(
            err => {
              ElMessage.error("注册失败")
            }
        )


      }

    },
  },
};
</script>

<style scoped>
.login {
  width: 100vw;
  height: 100vh;
  font-size: 16px;
  background-position: left top;
  background-color: #242645;
  color: #fff;
  font-family: "Source Sans Pro";
  position: relative;
}

.mylogin {
  width: 240px;
  height: 280px;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: auto;
  padding: 50px 40px 40px 40px;
  box-shadow: -15px 15px 15px rgba(6, 17, 47, 0.7);
  opacity: 1;
  background: linear-gradient(
      230deg,
      rgba(53, 57, 74, 0) 0%,
      rgb(0, 0, 0) 100%
  );
}

.inps input {
  border: none;
  color: #fff;
  background-color: transparent;
  font-size: 12px;
}

.submitBtn {
  background-color: transparent;
  color: #39f;
  width: 200px;
}
</style>