import API from '@/api/mack.js'

export default {
    successCide: 200,
    group: {
        apiObj: API.userOrgTreeSelector,
        parseData: function (res) {
            return {
                rows: res.data,
                msg: res.msg,
                code: res.code
            }
        },
        //显示数据字段映射
        props: {
            key: 'id',
            label: 'label',
            children: 'children'
        }
    },
    //配置用户
    user: {
        apiObj: API.userSelector,
        pageSize: 20,
        parseData: function (res) {
            return {
                rows: res.data.rows,
                total: res.data.total,
                msg: res.msg,
                code: res.code
            }
        },
        props: {
            key: 'id',
            label: 'user'
        },
        request: {
            page: 'page',
            pageSize: 'pageSize',
            groupId: 'groupId',
            keyword: 'keyword'
        }
    },
    //配置角色
    role: {
        //请求接口对象
        apiObj: API.userRoleSelector,
        //接受数据字段映射
        parseData: function (res) {
            return {
                rows: res.data,
                msg: res.msg,
                code: res.code
            }
        },
        //显示数据字段映射
        props: {
            key: 'id',
            label: 'label',
            children: 'children'
        }
    }
}