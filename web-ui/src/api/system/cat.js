import request from '@/utils/request'

// 查询资讯分类列表
export function listCat(query) {
    return request({
        url: '/erp/cat/list',
        method: 'get',
        params: query
    })
}

// 查询资讯分类详细
export function getCat(id) {
    return request({
        url: '/erp/cat/' + id,
        method: 'get'
    })
}

// 新增资讯分类
export function addCat(data) {
    return request({
        url: '/erp/cat',
        method: 'post',
        data: data
    })
}

// 修改资讯分类
export function updateCat(data) {
    return request({
        url: '/erp/cat',
        method: 'put',
        data: data
    })
}

// 删除资讯分类
export function delCat(id) {
    return request({
        url: '/erp/cat/' + id,
        method: 'delete'
    })
}
