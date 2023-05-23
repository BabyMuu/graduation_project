# sysman

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```


```css

分类单独抽出来个表 ( 可以做一个假的 ) sort 表
字段 
	id			// ID 唯一标识
	name		// 分类名称  对应 商品表中的 sort 字段
	create_time
	update_time

"/sort" 
	路由 get 请求
		返回结构
			data:{
				id:
				name:
				count:         	// 该分类下的商品数量
				create_time
				update_time
			}
	路由 post 请求
		请求结构
			{
				name
			}
		返回结构
			状态码 200 成功
			状态码 400 失败
	路由 delete 请求
		请求结构
			{
				id
			}
		返回结构
			状态码 200 成功
			状态码 400 失败
			
"/account"
	路由 put 请求
        注: 用户名在header中获取
		请求结构1
			{
				phoneNum
			}
		返回结构
			状态码 200 成功
			状态码 400 失败



"/orderHistory"
	路由 get 请求
		注: 用户名在header中获取
		请求结构
			{
				page: 当前页数 (从 1 开始)
			}
		返回结构
			{
				orders: 查询出来的历史订单 分页 一页最多12条
				count: 该用户的历史订单总数
			}
			
"/dashboard"
	路由 get 请求
		返回结构
			{
				orderTotal  : 订单总数
				orderReg    : 三十天内的订单数量
				userTotal   : 用户总数
				userReg     : 三十天内的用户注册量
				orderTotalPoint : 订单月增长比率
				orderRegPoint   : 相对上个月订单增长比率
				userTotalPoint  : 用户月增长比率
				userRegPoint    : 相对上个月用户增长比率
				users:[
				    username    : 用户名
                    difTime     : 注册时间(分钟)
                    icon        : 用户头像
				]
				chartData: {
					user :{
						data : 横轴数据-日期(按日)
						stat : 纵轴数据-日增人数
					},
					order: {
						data : 横轴数据-日期(按日)
						stat : 纵轴数据-日订单量
					},
					orderStat: {
						value : 订单数量
						name : 品类名称
					},
					orderTotal: {
						data : 横轴数据-年月(按月) 从 2022-01 开始
						stat : 纵轴数据-月订单量
					}
				}
			}
```