import request from '@/utils/request'

// 查询企业工商数据列表
export function listInformation(query) {
    return request({
        url: '/erp/information/list',
        method: 'get',
        params: query
    })
}

// 查询企业工商数据详细
export function getInformation(id) {
    return request({
        url: '/erp/information/' + id,
        method: 'get'
    })
}

// 新增企业工商数据
export function addInformation(data) {
    return request({
        url: '/erp/information',
        method: 'post',
        data: data
    })
}

// 修改企业工商数据
export function updateInformation(data) {
    return request({
        url: '/erp/information',
        method: 'put',
        data: data
    })
}

// 删除企业工商数据
export function delInformation(id) {
    return request({
        url: '/erp/information/' + id,
        method: 'delete'
    })
}
