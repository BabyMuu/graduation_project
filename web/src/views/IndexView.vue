<script setup>
import {RouterLink, RouterView} from 'vue-router'
import Menu from '@/components/Menu.vue'
</script>

<template>
  <div id="app">
    <el-container class="home-container">
      <el-header id="title">
        <img alt="Vue logo" src="@/assets/logo.svg"/>
        <span id="title" style="color: yellow">𝓑𝓪𝓬𝓴𝓰𝓻𝓸𝓾𝓷𝓭 𝓶𝓪𝓷𝓪𝓰𝓮𝓶𝓮𝓷𝓽 𝓼𝔂𝓼𝓽𝓮𝓶</span>
        <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            @select="handleSelect"
            style="float: right"
            background-color="#2c3e50"
            text-color="greenyellow"
            :ellipsis="false"
        >
          <el-menu-item index="1" @click="this.$router.push('/dashboard')">Processing Center</el-menu-item>

          <el-menu-item index="3">{{ username }}
            <el-sub-menu :popper-offset="1" id="info">
              <el-menu-item index="account" @click="this.$router.push('/account')">个人信息
              </el-menu-item>
              <el-menu-item index="logout" @click="this.$router.push('/login'); localStorage.clear()">登出
              </el-menu-item>
              <el-menu-item index="changePassword" @click="this.$router.push('/account')">修改密码</el-menu-item>
            </el-sub-menu>
          </el-menu-item>
        </el-menu>
      </el-header>
      <el-container>
        <el-aside id="aside">
          <Menu/>
        </el-aside>
        <el-aside width="1px" style="background-color: white; height: 100%"></el-aside>
        <el-main id="main" style="background-color: #f5f5f5">
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>


import {mapState} from "vuex";

export default {
  name: "IndexView",
  computed: {
    ...mapState(['username']),
  },
}
</script>

<style scoped>
#app {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.home-container {
  height: 100%;
}

#title {
  background-color: #2c3e50;
}

#info > el-menu-item {
  color: #1E9FFF;
  text-align: center;
}

#title > img {
  margin-top: 15px;
  align-items: center;
  width: 40px;
}

#title > span {
  font-size: 30px;
  color: white;
  margin-left: 15px;
}

#aside {
  background-color: #545c64;
  width: 200px;
  height: 100%
}

#main {
  height: 100%;
  /*background-color: gray;*/
}
</style>