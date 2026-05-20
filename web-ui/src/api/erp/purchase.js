import request from '@/utils/request'

// 查询采购单主列表
export function listPurchase(query) {
    return request({
        url: '/erp/purchase/list',
        method: 'get',
        params: query
    })
}

// 查询采购单主详细
export function getPurchase(id) {
    return request({
        url: '/erp/purchase/' + id,
        method: 'get'
    })
}

// 新增采购单主
export function addPurchase(data) {
    return request({
        url: '/erp/purchase',
        method: 'post',
        data: data
    })
}

// 修改采购单主
export function updatePurchase(data) {
    return request({
        url: '/erp/purchase',
        method: 'put',
        data: data
    })
}

// 删除采购单主
export function delPurchase(id) {
    return request({
        url: '/erp/purchase/' + id,
        method: 'delete'
    })
}
