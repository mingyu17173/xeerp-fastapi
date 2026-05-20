import request from '@/utils/request'

// 查询资讯列表
export function listArticle(query) {
    return request({
        url: '/system/article/list',
        method: 'get',
        params: query
    })
}

// 查询资讯详细
export function getArticle(id) {
    return request({
        url: '/system/article/' + id,
        method: 'get'
    })
}

// 新增资讯
export function addArticle(data) {
    return request({
        url: '/system/article',
        method: 'post',
        data: data
    })
}

// 修改资讯
export function updateArticle(data) {
    return request({
        url: '/system/article',
        method: 'put',
        data: data
    })
}

// 删除资讯
export function delArticle(id) {
    return request({
        url: '/system/article/' + id,
        method: 'delete'
    })
}
