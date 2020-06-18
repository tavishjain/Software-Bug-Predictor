import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex);
import metricsJson from './../../../../conf/translations/metrics.json';

export default new Vuex.Store({
  state: {
    pageName: 'Understand',
    translatedLanguages: [
      'en',
      'ja'
    ],
    metricDefinitions: metricsJson,
    selectedMetric: null,
    showDialog: false,
    lang: 'en',
  },
  mutations: {
    updateMetricDefinitions(state, metricDefinitions){
      state.metricDefinitions =  metricDefinitions;
    } ,
    updatePageName(state, pageName){
      state.pageName =  pageName;
    },
    updateLang(state, lang){
      if(state.translatedLanguages.includes(lang)) {
        state.lang = lang;
      }
    },
    updateSelectedMetric(state, selectedMetric){
      state.selectedMetric =  selectedMetric;
    },
    updateShowDialog(state, show){
      state.showDialog =  show;
    }
  },
  actions: {
  },
  modules: {
  }
})
