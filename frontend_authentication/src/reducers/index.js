import { combineReducers } from 'redux'
import {  connectRouter } from 'connected-react-router'

import authReducer from './authReducer'


const createRootReducer = (history) => combineReducers({
  router: connectRouter(history),
  authReducer
})
export default createRootReducer;