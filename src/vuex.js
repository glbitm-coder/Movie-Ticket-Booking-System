import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
      isAuthenticated: false,
      access_token: localStorage.getItem('access_token') || null,
      expiryTime: localStorage.getItem('expiryTine'),
      notification: null
    },
    mutations: {
      setAuthentication(state, payload) {
        state.isAuthenticated = payload.isAuthenticated;
      },
      setToken(state, payload) {
        state.access_token = payload.access_token;
        localStorage.setItem('access_token', payload.access_token);
      },
      setExpiryTime(state, payload){
        state.expiryTime = payload.expiryTime;
        localStorage.setItem('expiryTime', payload.expiryTime);
      },
      setNotification(state, { variant, message }) {
        state.notification = { variant, message };
      },
      clearNotification(state) {
        state.notification = null;
      }
    }
  });
  

  export default store;