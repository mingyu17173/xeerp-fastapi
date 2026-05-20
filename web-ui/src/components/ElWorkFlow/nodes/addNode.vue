<template>
    <div class="add-node-btn-box">
        <div class="add-node-btn">
            <el-popover placement="right" :width="100" trigger="click" :hide-after="0" :show-after="0">
                <template #reference>
                    <el-button type="primary" icon="plus" circle></el-button>
                </template>
                <div class="add-node-popover-body">
                    <ul style="padding: 0px;">
                        <li>
                            <el-icon style="color: #ff943e;" @click="addType(1)">
                                <UserFilled/>
                            </el-icon>
                            <p>审批节点</p>
                        </li>
                        <li>
                            <el-icon style="color: #3296fa;" @click="addType(2)">
                                <Promotion/>
                            </el-icon>
                            <p>抄送节点</p>
                        </li>
                        <li>
                            <el-icon style="color: #15BC83;" @click="addType(4)">
                                <Share/>
                            </el-icon>
                            <p>条件分支</p>
                        </li>
                    </ul>
                </div>
            </el-popover>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
        modelValue: {
            type: Object,
            default: () => {
            }
        }
    })
    const emit = defineEmits(['update'])


    const addType = (type) => {
        let node = {}
        if (type === 1) {
            node = {
                nodeName: "审核人",
                type: 1,			//节点类型
                setType: 1,			//审核人类型 1，选择成员 3，选择角色
                nodeAssigneeList: [],	//审核人员，根据 setType 确定成员还是角色
                examineLevel: 1,	//指定主管层级
                directorLevel: 1,	//自定义连续主管审批层级
                selectMode: 1,		//发起人自选类型
                termAuto: false,	//审批期限超时自动审批
                term: 0,			//审批期限
                termMode: 1,		//审批期限超时后执行类型
                examineMode: 1,		//多人审批时审批方式
                directorMode: 0,	//连续主管审批方式
                childNode: props.modelValue
            }
        } else if (type === 2) {
            node = {
                nodeName: "审核人",
                type: 1,
                userSelectFlag: true,
                nodeAssigneeList: [],
                childNode: props.modelValue
            }
        } else if (type === 4) {
            node = {
                nodeName: "条件路由",
                type: 4,
                conditionNodes: [
                    {
                        nodeName: "条件1",
                        type: 3,
                        priorityLevel: 1,
                        conditionMode: 1,
                        conditionList: []
                    },
                    {
                        nodeName: "条件2",
                        type: 3,
                        priorityLevel: 2,
                        conditionMode: 1,
                        conditionList: []
                    }
                ],
                childNode: this.modelValue
            }
        }
        emit("update:modelValue", node);
    }
</script>