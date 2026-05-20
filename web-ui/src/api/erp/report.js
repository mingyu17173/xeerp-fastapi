import request from '@/utils/request'

// 查询采购库存列表
export function listReport(query) {
    return request({
        url: '/erp/report/list',
        method: 'get',
        params: query
    })
}

// 查询采购库存详细
export function getReport(id) {
    return request({
        url: '/erp/report/' + id,
        method: 'get'
    })
}

// 新增采购库存
export function addReport(data) {
    return request({
        url: '/erp/report',
        method: 'post',
        data: data
    })
}

// 修改采购库存
export function updateReport(data) {
    return request({
        url: '/erp/report',
        method: 'put',
        data: data
    })
}

// 删除采购库存
export function delReport(id) {
    return request({
        url: '/erp/report/' + id,
        method: 'delete'
    })
}
