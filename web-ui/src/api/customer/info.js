import request from '@/utils/request'

// 查询客户信息列表
export function listInfo(query) {
  return request({
    url: '/customer/info/list',
    method: 'get',
    params: query
  })
}

// 查询客户信息详细
export function getInfo(customerId) {
  return request({
    url: '/customer/info/' + customerId,
    method: 'get'
  })
}

// 新增客户信息
export function addInfo(data) {
  return request({
    url: '/customer/info',
    method: 'post',
    data: data
  })
}

// 修改客户信息
export function updateInfo(data) {
  return request({
    url: '/customer/info',
    method: 'put',
    data: data
  })
}

// 删除客户信息
export function delInfo(customerId) {
  return request({
    url: '/customer/info/' + customerId,
    method: 'delete'
  })
}
