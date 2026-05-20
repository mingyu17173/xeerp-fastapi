import request from '@/utils/request'

// 查询产品基本信息列表
export function listProduct(query) {
    return request({
        url: '/system/product/list',
        method: 'get',
        params: query
    })
}

// 查询产品基本信息详细
export function getProduct(id) {
    return request({
        url: '/system/product/' + id,
        method: 'get'
    })
}

// 新增产品基本信息
export function addProduct(data) {
    return request({
        url: '/system/product',
        method: 'post',
        data: data
    })
}

// 修改产品基本信息
export function updateProduct(data) {
    return request({
        url: '/system/product',
        method: 'put',
        data: data
    })
}

// 删除产品基本信息
export function delProduct(id) {
    return request({
        url: '/system/product/' + id,
        method: 'delete'
    })
}
