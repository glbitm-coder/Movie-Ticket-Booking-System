import SignUp from './components/SignUp.vue'
import Home from './components/Home.vue'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import store from './vuex';
import VueRouter from 'vue-router'

const routes = [
    {
        name : 'SignUp',
        component : SignUp,
        path : '/signup',
        meta: { 
            requiresGuest: true 
        }
    },
    {
        name : 'Home',
        component : Home,
        path : '/'
    },
    {
        name : 'Login',
        component : Login,
        path : '/login',
        meta: { 
            requiresGuest: true 
        }
    },
    {
        name : 'Dashboard',
        component : Dashboard,
        path : '/dashboard',
        meta: {
            requiresAuth: true
        }
    }
];

const router = new VueRouter({
    routes
})


router.beforeEach(async (to, from, next) => {
    const isAuthenticated = store.state.isAuthenticated;
    const requiresAuth = to.meta.requiresAuth;
    const requiresGuest = to.meta.requiresGuest;

    if (requiresAuth && !isAuthenticated) {
      next('/');
    } else if (requiresGuest && isAuthenticated) {
      next('/dashboard');
    } else {
      const accessToken = store.state.access_token;
      const expiryTime = store.state.expiryTime;
  
      if (requiresAuth && accessToken && expiryTime) {
        const currentTime = Date.now();
        const tokenExpired = currentTime > new Date(expiryTime);
  
        if (tokenExpired) {
          await store.dispatch('logout');
          next('/');
        } else {
          store.commit('setAuthentication', { isAuthenticated: true });
          store.commit('setToken', { access_token: accessToken });
          store.commit('setExpiryTime', { expiryTime : expiryTime })
          next();
        }
      } else {
        next();
      }
    }
  });

export default router;