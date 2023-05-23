<script setup>
import {
  Document, Menu as IconMenu,
  Location,
  Setting,
  Star,
  User,
  Operation,
  GoodsFilled,
  Sort
} from "@element-plus/icons-vue";
</script>
<template>
  <el-row>
    <el-col>
      <el-menu
          active-text-color="#ffd04b"
          default-active="2"
          text-color="#fff"
          background-color="#545c64"
          @open="handleOpen"
          @close="handleClose"
          router
      >
        <el-menu-item index="dashboard">
          <template #title>
            <el-icon>
              <Star/>
            </el-icon>
            <span>概述</span>
          </template>
        </el-menu-item>
        <el-menu-item index="user">
          <template #title>
            <el-icon>
              <location/>
            </el-icon>
            <span>学生管理</span>
          </template>
        </el-menu-item>
        <el-sub-menu index="permissions">
          <template #title>
            <el-icon>
              <IconMenu/>
            </el-icon>
            <span>考试管理</span>
          </template>
          <el-menu-item index="score">
            <el-icon>
              <User/>
            </el-icon>
            <span>分数详情</span>
          </el-menu-item>
          <el-menu-item index="exam">
            <el-icon>
              <Operation/>
            </el-icon>
            考试分析
          </el-menu-item>
        </el-sub-menu>
<!--        <el-menu-item index="order">-->
<!--          <el-icon>-->
<!--            <document/>-->
<!--          </el-icon>-->
<!--          <span>订单管理</span>-->
<!--        </el-menu-item>-->
<!--        <el-sub-menu index="good">-->
<!--          <template #title>-->
<!--            <el-icon>-->
<!--              <setting/>-->
<!--            </el-icon>-->
<!--            <span>商品管理</span>-->
<!--          </template>-->
<!--          <el-menu-item index="goods">-->
<!--            <el-icon>-->
<!--              <GoodsFilled/>-->
<!--            </el-icon>-->
<!--            商品列表-->
<!--          </el-menu-item>-->
<!--          <el-menu-item index="good-sort">-->
<!--            <el-icon>-->
<!--              <Sort/>-->
<!--            </el-icon>-->
<!--            分类管理-->
<!--          </el-menu-item>-->
<!--        </el-sub-menu>-->
      </el-menu>
    </el-col>
  </el-row>
</template>
<script>
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  name: "Menu",
  data() {
    return {
      mainMenu: []
    }
  },
  methods: {
    handleOpen(key, keyPath) {

    },
    handleClose(key, keyPath) {

    }
  },

  created() {
    axios.get("/mainMenu").then(
        res => {

        }
    ).catch(
        error => {
          ElMessage.error("请求菜单失败, 请在网络状态良好的情况下重新加载本页")
        }
    )
  }
}

</script>
