import Vue from 'vue'
import VueRouter from 'vue-router'
import ImageInfoPage from '@/components/ImageInfoPage'
// import ExhibitBoard from '@/components/ExhibitBoard'
import ExhibitPage from "@/components/ExhibitPage"
import RepairInfoPage from '@/components/RepairInfoPage'
import PhotoList from '@/components/PhotoList'
import GalleryList from '@/components/GalleryList'
import UserHome from '@/components/UserHome'
import AdminTest from '@/views/AdminTest'
import Login from '@/views/Login'
import PhotoAdmin from '@/components/PhotoAdmin'
import UserList from '@/components/UserList'
import SearchResultPage from '@/components/SearchResultPage'
// import GalleryList from '@/components/GalleryList'
// import NewGallery from '@/components/NewGallery'
import ExhibitAdmin from '@/components/ExhibitAdmin'
import ExhibitEditPage from '@/components/ExhibitEditPage'
import ChangeInfo from '@/components/ChangeInfo'
import PhotosEditPage from '@/components/PhotosEditPage'
import Dealcomment from '@/components/Dealcomment'
Vue.use(VueRouter);

// 定义路由
const routes = [
    { path: '/search', component: SearchResultPage, name: 'search'},
    { path: '/exhibits', component: ExhibitPage },
    { path: '/', component: UserHome, name: 'home'},
    { path: '/image/:id', component: ImageInfoPage , name: 'image', props: true},
    { path: '/exhibit/:id', component: ExhibitPage , name: 'exhibit', props: true},
    { path: '/repair/:id', component: RepairInfoPage , name: 'repair', props: true},
    { path: '/admin', component: AdminTest, name: 'admin', children: [
      {
        path: 'photo',
        name: 'photo',
        component: PhotoAdmin
      },
      {
        path: 'editphoto',
        name: 'editphoto',
        component: PhotosEditPage
      },
      {
        path: 'gallery',
        name: 'gallery',
        component: ExhibitAdmin,
      },
      {
        path: 'editgellery',
        name: 'editgellery',
        component: PhotosEditPage
      },
      {
        path: 'user',
        name: 'user',
        component: UserList
      },
      { path: 'dealcomment', component: Dealcomment , name: 'dealcomment'},
      // { path: 'fix', component: FixPhoto, name: "fix_photo" },
      { path: 'gallerylist', component: GalleryList, name: 'GalleryList'},
      // { path: 'addgallery', component: NewGallery, name: 'new_gallery'},
      { path: 'past', component: PhotoList ,name: "past"},
      { path: 'changelist', component: ChangeInfo , name:"changeinfo"},
      { path: 'exhibit/:id', component: ExhibitEditPage , name: 'exhibit_edit', props: true},
    ]},
    { path: '/login', component: Login},
    
    // { path: '/about', component: About },
  ]

const router = new VueRouter({
	mode: 'history',
    //VueRouter.createWebHashHistory(),
	routes,
  // 添加配置：router切换时，回到屏幕顶端
  scrollBehavior(to,from,savedPosition){
    if(savedPosition){
      return savedPosition
    }
    else{
      return{
        x:0,
        y:0
      }
    }
  }
})

export default router