import { createStore } from 'vuex';
import darkMode from './modules/darkMode';
import sideBar from './modules/sideBar';
import token from './modules/token';

export default createStore({
  modules: {
    darkMode,
    sideBar,
    token,
  },
  strict: true, // Enforce best practices in development
});
