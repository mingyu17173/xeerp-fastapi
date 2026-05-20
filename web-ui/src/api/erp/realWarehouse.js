import request from '@/utils/request'

// 查询实体仓库列表
export function listWarehouse(query) {
    return request({
        url: '/erp/real/warehouse/list',
        method: 'get',
        params: query
    })
}

// 查询实体仓库详细
export function getWarehouse(id) {
    return request({
        url: '/erp/real/warehouse/' + id,
        method: 'get'
    })
}

// 新增实体仓库
export function addWarehouse(data) {
    return request({
        url: '/erp/real/warehouse',
        method: 'post',
        data: data
    })
}

// 修改实体仓库
export function updateWarehouse(data) {
    return request({
        url: '/erp/real/warehouse',
        method: 'put',
        data: data
    })
}

// 删除实体仓库
export function delWarehouse(id) {
    return request({
        url: '/erp/real/warehouse/' + id,
        method: 'delete'
    })
}
