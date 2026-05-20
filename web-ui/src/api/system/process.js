import request from '@/utils/request'

// 查询流程定义列表
export function listProcess(query) {
    return request({
        url: '/system/process/list',
        method: 'get',
        params: query
    })
}

// 查询流程定义详细
export function getProcess(id) {
    return request({
        url: '/system/process/' + id,
        method: 'get'
    })
}

// 新增流程定义
export function addProcess(data) {
    return request({
        url: '/system/process',
        method: 'post',
        data: data
    })
}

// 修改流程定义
export function updateProcess(data) {
    return request({
        url: '/system/process',
        method: 'put',
        data: data
    })
}

// 删除流程定义
export function delProcess(id) {
    return request({
        url: '/system/process/' + id,
        method: 'delete'
    })
}
