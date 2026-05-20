import request from '@/utils/request'

// 查询合作伙伴银行列表
export function listBank(query) {
    return request({
        url: '/erp/bank/list',
        method: 'get',
        params: query
    })
}

// 查询合作伙伴银行详细
export function getBank(id) {
    return request({
        url: '/erp/bank/' + id,
        method: 'get'
    })
}

// 新增合作伙伴银行
export function addBank(data) {
    return request({
        url: '/erp/bank',
        method: 'post',
        data: data
    })
}

// 修改合作伙伴银行
export function updateBank(data) {
    return request({
        url: '/erp/bank',
        method: 'put',
        data: data
    })
}

// 删除合作伙伴银行
export function delBank(id) {
    return request({
        url: '/erp/bank/' + id,
        method: 'delete'
    })
}
