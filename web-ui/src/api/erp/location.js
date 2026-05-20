import request from '@/utils/request'

// 查询虚拟仓位列表
export function listLocation(query) {
    return request({
        url: '/erp/location/list',
        method: 'get',
        params: query
    })
}

// 查询虚拟仓位详细
export function getLocation(id) {
    return request({
        url: '/erp/location/' + id,
        method: 'get'
    })
}

// 新增虚拟仓位
export function addLocation(data) {
    return request({
        url: '/erp/location',
        method: 'post',
        data: data
    })
}

// 修改虚拟仓位
export function updateLocation(data) {
    return request({
        url: '/erp/location',
        method: 'put',
        data: data
    })
}

// 删除虚拟仓位
export function delLocation(id) {
    return request({
        url: '/erp/location/' + id,
        method: 'delete'
    })
}
