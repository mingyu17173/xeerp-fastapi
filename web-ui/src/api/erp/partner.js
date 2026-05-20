import request from '@/utils/request'

// 查询商业伙伴列表
export function listPartner(query) {
    return request({
        url: '/crm/partner/list',
        method: 'get',
        params: query
    })
}

// 查询商业伙伴详细
export function getPartner(id) {
    return request({
        url: '/erp/partner/' + id,
        method: 'get'
    })
}

// 新增商业伙伴
export function addPartner(data) {
    return request({
        url: '/erp/partner',
        method: 'post',
        data: data
    })
}

// 修改商业伙伴
export function updatePartner(data) {
    return request({
        url: '/erp/partner',
        method: 'put',
        data: data
    })
}

// 删除商业伙伴
export function delPartner(id) {
    return request({
        url: '/erp/partner/' + id,
        method: 'delete'
    })
}
