import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import router from './router'
import 'jquery'
import { Icon,Steps,Button } from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
Vue.component(Icon.name, Icon);
Vue.component(Steps.name, Steps);
Vue.component(Steps.Step.name, Steps.Step);
Vue.component(Button.name,Button);
Vue.use(ElementUI);
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')





