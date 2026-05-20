import request from '@/utils/request'

// 查询虚拟仓库列表
export function listWarehouse(query) {
    return request({
        url: '/erp/virtual/warehouse/list',
        method: 'get',
        params: query
    })
}

// 查询虚拟仓库详细
export function getWarehouse(id) {
    return request({
        url: '/erp/virtual/warehouse/' + id,
        method: 'get'
    })
}

// 新增虚拟仓库
export function addWarehouse(data) {
    return request({
        url: '/erp/virtual/warehouse',
        method: 'post',
        data: data
    })
}

// 修改虚拟仓库
export function updateWarehouse(data) {
    return request({
        url: '/erp/virtual/warehouse',
        method: 'put',
        data: data
    })
}

// 删除虚拟仓库
export function delWarehouse(id) {
    return request({
        url: '/erp/virtual/warehouse/' + id,
        method: 'delete'
    })
}
