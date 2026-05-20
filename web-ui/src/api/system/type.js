import request from '@/utils/request'

// 查询单据类型列表
export function listType(query) {
    return request({
        url: '/system/type/list',
        method: 'get',
        params: query
    })
}

// 查询单据类型详细
export function getType(id) {
    return request({
        url: '/system/type/' + id,
        method: 'get'
    })
}

// 新增单据类型
export function addType(data) {
    return request({
        url: '/system/type',
        method: 'post',
        data: data
    })
}

// 修改单据类型
export function updateType(data) {
    return request({
        url: '/system/type',
        method: 'put',
        data: data
    })
}

// 删除单据类型
export function delType(id) {
    return request({
        url: '/system/type/' + id,
        method: 'delete'
    })
}
