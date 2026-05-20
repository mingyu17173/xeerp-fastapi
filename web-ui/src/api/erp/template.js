import request from '@/utils/request'

// 查询合同模版列表
export function listTemplate(query) {
    return request({
        url: '/erp/template/list',
        method: 'get',
        params: query
    })
}

// 查询合同模版详细
export function getTemplate(templateId) {
    return request({
        url: '/erp/template/' + templateId,
        method: 'get'
    })
}

// 新增合同模版
export function addTemplate(data) {
    return request({
        url: '/erp/template',
        method: 'post',
        data: data
    })
}

// 修改合同模版
export function updateTemplate(data) {
    return request({
        url: '/erp/template',
        method: 'put',
        data: data
    })
}

// 删除合同模版
export function delTemplate(templateId) {
    return request({
        url: '/erp/template/' + templateId,
        method: 'delete'
    })
}
