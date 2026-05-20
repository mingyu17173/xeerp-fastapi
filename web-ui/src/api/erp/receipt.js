import request from '@/utils/request'

// 查询收款单列表
export function listReceipt(query) {
    return request({
        url: '/erp/receipt/list',
        method: 'get',
        params: query
    })
}

// 查询收款单详细
export function getReceipt(id) {
    return request({
        url: '/erp/receipt/' + id,
        method: 'get'
    })
}

// 新增收款单
export function addReceipt(data) {
    return request({
        url: '/erp/receipt',
        method: 'post',
        data: data
    })
}

// 修改收款单
export function updateReceipt(data) {
    return request({
        url: '/erp/receipt',
        method: 'put',
        data: data
    })
}

// 删除收款单
export function delReceipt(id) {
    return request({
        url: '/erp/receipt/' + id,
        method: 'delete'
    })
}
