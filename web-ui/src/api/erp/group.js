import request from '@/utils/request'

// 查询虚拟仓库组列表
export function listGroup(query) {
    return request({
        url: '/erp/group/list',
        method: 'get',
        params: query
    })
}

// 查询虚拟仓库组详细
export function getGroup(id) {
    return request({
        url: '/erp/group/' + id,
        method: 'get'
    })
}

// 新增虚拟仓库组
export function addGroup(data) {
    return request({
        url: '/erp/group',
        method: 'post',
        data: data
    })
}

// 修改虚拟仓库组
export function updateGroup(data) {
    return request({
        url: '/erp/group',
        method: 'put',
        data: data
    })
}

// 删除虚拟仓库组
export function delGroup(id) {
    return request({
        url: '/erp/group/' + id,
        method: 'delete'
    })
}
