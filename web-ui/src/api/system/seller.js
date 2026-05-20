import request from '@/utils/request'

// 查询公司列表列表
export function listSeller(query) {
    return request({
        url: '/system/seller/list',
        method: 'get',
        params: query
    })
}

// 查询公司列表详细
export function getSeller(id) {
    return request({
        url: '/system/seller/' + id,
        method: 'get'
    })
}

// 新增公司列表
export function addSeller(data) {
    return request({
        url: '/system/seller',
        method: 'post',
        data: data
    })
}

// 修改公司列表
export function updateSeller(data) {
    return request({
        url: '/system/seller',
        method: 'put',
        data: data
    })
}

// 删除公司列表
export function delSeller(id) {
    return request({
        url: '/system/seller/' + id,
        method: 'delete'
    })
}
