import request from '@/utils/request'

// 查询调拨单列表
export function listMove(query) {
    return request({
        url: '/erp/move/list',
        method: 'get',
        params: query
    })
}

// 查询调拨单详细
export function getMove(id) {
    return request({
        url: '/erp/move/' + id,
        method: 'get'
    })
}

// 新增调拨单
export function addMove(data) {
    return request({
        url: '/erp/move',
        method: 'post',
        data: data
    })
}

// 修改调拨单
export function updateMove(data) {
    return request({
        url: '/erp/move',
        method: 'put',
        data: data
    })
}

// 删除调拨单
export function delMove(id) {
    return request({
        url: '/erp/move/' + id,
        method: 'delete'
    })
}
