import request from '@/utils/request'

// 查询地址区域列表
export function listRegion(query) {
    return request({
        url: '/system/region/list',
        method: 'get',
        params: query
    })
}

// 查询地址区域详细
export function getRegion(id) {
    return request({
        url: '/system/region/' + id,
        method: 'get'
    })
}

// 新增地址区域
export function addRegion(data) {
    return request({
        url: '/system/region',
        method: 'post',
        data: data
    })
}

// 修改地址区域
export function updateRegion(data) {
    return request({
        url: '/system/region',
        method: 'put',
        data: data
    })
}

// 删除地址区域
export function delRegion(id) {
    return request({
        url: '/system/region/' + id,
        method: 'delete'
    })
}
