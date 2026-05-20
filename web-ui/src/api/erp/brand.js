import request from '@/utils/request'

// 查询产品厂商列表
export function listBrand(query) {
    return request({
        url: '/erp/brand/list',
        method: 'get',
        params: query
    })
}

// 查询产品厂商详细
export function getBrand(id) {
    return request({
        url: '/erp/brand/' + id,
        method: 'get'
    })
}

// 新增产品厂商
export function addBrand(data) {
    return request({
        url: '/erp/brand',
        method: 'post',
        data: data
    })
}

// 修改产品厂商
export function updateBrand(data) {
    return request({
        url: '/erp/brand',
        method: 'put',
        data: data
    })
}

// 删除产品厂商
export function delBrand(id) {
    return request({
        url: '/erp/brand/' + id,
        method: 'delete'
    })
}
