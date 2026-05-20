<template>
    <div class="node-wrap">
        <div class="node-wrap-box" @click="show">
            <div class="title" style="background: #3296fa;">
                <el-icon class="icon">
                    <Promotion/>
                </el-icon>
                />
                <span>{{ nodeConfig.nodeName }}</span>
                <el-icon class="close" @click.stop="delNode()">
                    <CircleClose/>
                </el-icon>
            </div>
            <div class="content">
                <span v-if="toText(nodeConfig)">{{ toText(nodeConfig) }}</span>
                <span v-else class="placeholder">请选择人员</span>
            </div>
        </div>
        <add-node v-model="nodeConfig.childNode"></add-node>
        <el-drawer title="抄送人设置" v-model="drawer" destroy-on-close append-to-body :size="500">
            <template #header>
                <div class="node-wrap-drawer__title">
                    <label @click="editTitle" v-if="!isEditTitle">{{form.nodeName}}
                        <el-icon class="node-wrap-drawer__title-edit">
                            <Edit/>
                        </el-icon>
                    </label>
                    <el-input v-if="isEditTitle" ref="nodeTitle" v-model="form.nodeName" clearable @blur="saveTitle"
                              @keyup.enter="saveTitle"></el-input>
                </div>
            </template>
            <el-container>
                <el-main style="padding:0 20px 20px 20px">
                    <el-form label-position="top">
                        <el-form-item label="选择要抄送的人员">
                            <el-button type="primary" icon="plus" round @click="selectHandle(1, form.nodeAssigneeList)">
                                选择人员
                            </el-button>
                            <div class="tags-list">
                                <el-tag v-for="(user, index) in form.nodeAssigneeList" :key="user.id" closable
                                        @close="delUser(index)">{{user.name}}
                                </el-tag>
                            </div>
                        </el-form-item>
                        <el-form-item label="">
                            <el-checkbox v-model="form.userSelectFlag" label="允许发起人自选抄送人"></el-checkbox>
                        </el-form-item>
                    </el-form>
                </el-main>
                <el-footer>
                    <el-button type="primary" @click="save">保存</el-button>
                    <el-button @click="drawer=false">取消</el-button>
                </el-footer>
            </el-container>
        </el-drawer>
    </div>
</template>

<script setup>
    import {ref, inject, reactive, nextTick, getCurrentInstance} from "vue";

    import addNode from './addNode.vue'

    inject('select')

    const {proxy} = getCurrentInstance();

    const props = defineProps({
        modelValue: {
            type: Object,
            default: () => {
            }
        }
    })

    const emit = defineEmits(['update'])

    const state = reactive({
        nodeConfig: {},
        drawer: false,
        isEditTitle: false,
        form: {}
    })

    const {nodeConfig, drawer, isEditTitle, form} = toRefs(state)

    watch(() => props.modelValue, value => state.nodeConfig = value)

    onMounted(() => {
        state.nodeConfig = props.modelValue
    })

    const show = () => {
        state.form = {}
        state.form = JSON.parse(JSON.stringify(this.nodeConfig))
        state.drawer = true
    }

    const editTitle = async () => {
        state.isEditTitle = true
        await nextTick(() => {
            proxy.$refs.nodeTitle.focus()
        })
    }

    const saveTitle = () => {
        state.isEditTitle = false
    }

    const save = () => {
        emit("update:modelValue", state.form)
        state.drawer = false
    }

    const delNode = () => {
        emit("update:modelValue", state.nodeConfig.childNode)
    }

    const delUser = (index) => {
        state.form.nodeAssigneeList.splice(index, 1)
    }

    const selectHandle = (type, data) => {
        props.select(type, data)
    }

    const toText = (nodeConfig) => {
        if (nodeConfig.nodeAssigneeList && nodeConfig.nodeAssigneeList.length > 0) {
            const users = nodeConfig.nodeAssigneeList.map(item => item.name).join("、")
            return users
        } else {
            if (nodeConfig.userSelectFlag) {
                return "发起人自选"
            } else {
                return false
            }
        }
    }
</script>