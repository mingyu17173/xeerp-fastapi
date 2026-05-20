<template>
    <div class="navbar">
        <minLogo v-if="sidebar.hide" :collapse="isCollapse"/>
        <hamburger id="hamburger-container" :is-active="appStore.sidebar.opened" class="hamburger-container"
                   @toggleClick="toggleSideBar"/>
        <breadcrumb id="breadcrumb-container" class="breadcrumb-container" v-if="!settingsStore.topNav"/>
        <top-nav id="topmenu-container" class="topmenu-container" v-if="settingsStore.topNav"/>

        <div class="right-menu">
            <template v-if="appStore.device !== 'mobile'">
                <!-- <header-search id="header-search" class="right-menu-item"/> -->

                <el-tooltip content="系统管理" effect="dark" placement="bottom">
                    <ruo-yi-settomgs class="right-menu-item hover-effect" v-hasPermi="['system:all']"/>
                </el-tooltip>

                <el-tooltip content="帮助文档" effect="dark" placement="bottom">
                    <ruo-yi-doc id="ruoyi-doc" class="right-menu-item hover-effect" v-hasPermi="['help:all']"
                                @click="dialogVisible"/>
                </el-tooltip>

                <el-tooltip content="开启Tags" effect="dark" placement="bottom">
                    <ruo-yi-crumb class="right-menu-item hover-effect"/>
                </el-tooltip>

            </template>
            <div class="avatar-container" style="background: rgba(0, 0, 0, 0.035);">
                <el-dropdown @command="handleCommand" class="right-menu-item hover-effect" trigger="click">
                    <div class="avatar-wrapper">
                        <img :src="userStore.avatar" class="user-avatar" :title="userStore.name"/>
                        <el-icon>
                            <caret-bottom/>
                        </el-icon>
                    </div>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="userInfo" disabled>
                                <span>{{userStore.name}}</span>
                            </el-dropdown-item>
                            <router-link to="/user/profile">
                                <el-dropdown-item divided>基本信息</el-dropdown-item>
                            </router-link>
                            <el-dropdown-item command="setLayout" v-if="settingsStore.showSettings">
                                <span>布局设置</span>
                            </el-dropdown-item>
                            <el-dropdown-item divided command="logout">
                                <span>退出登录</span>
                            </el-dropdown-item>
                            <el-dropdown-item disabled divided>
                                <span v-for="dict in sys_version"
                                      :key="dict.value"
                                      :label="dict.label"
                                      :value="dict.value">版本 V{{ dict.value }}</span>
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
        <!--帮助中心-->
        <HelpView v-model="isOpen" @closeHandle="handlerClose"></HelpView>
    </div>
</template>

<script setup>
    import {toRefs} from 'vue'
    import minLogo from './Sidebar/minLogo'
    import {ElMessageBox} from 'element-plus'
    import Breadcrumb from '@/components/Breadcrumb'
    import TopNav from '@/components/TopNav'
    import Hamburger from '@/components/Hamburger'
    import Screenfull from '@/components/Screenfull'
    import SizeSelect from '@/components/SizeSelect'
    import HeaderSearch from '@/components/HeaderSearch'
    import RuoYiGit from '@/components/RuoYi/Git'
    import RuoYiDoc from '@/components/RuoYi/Doc'
    import RuoYiCrumb from '@/components/RuoYi/Crumb'
    import RuoYiSettomgs from '@/components/RuoYi/Settings'
    import useAppStore from '@/store/modules/app'
    import useUserStore from '@/store/modules/user'
    import useSettingsStore from '@/store/modules/settings'
    import HelpView from './Help/index'

    const {proxy} = getCurrentInstance();
    const {sys_version} = proxy.useDict("sys_version");

    const store = reactive({
        isOpen: false
    })

    const {isOpen} = toRefs(store)

    const appStore = useAppStore()
    const userStore = useUserStore()
    const settingsStore = useSettingsStore()

    const sidebar = computed(() => useAppStore().sidebar);

    const sidebarRouters = computed(() => permissionStore.sidebarRouters);
    const showLogo = computed(() => settingsStore.sidebarLogo);
    const sideTheme = computed(() => settingsStore.sideTheme);
    const theme = computed(() => settingsStore.theme);
    const isCollapse = computed(() => !appStore.sidebar.opened);

    function toggleSideBar() {
        appStore.toggleSideBar()
    }

    function handleCommand(command) {
        switch (command) {
            case "setLayout":
                setLayout();
                break;
            case "logout":
                logout();
                break;
            default:
                break;
        }
    }

    function logout() {
        ElMessageBox.confirm('确定注销并退出系统吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            userStore.logOut().then(() => {
                location.href = '/index';
            })
        }).catch(() => {
        });
    }

    const emits = defineEmits(['setLayout'])

    function setLayout() {
        emits('setLayout');
    }

    // 案例
    const dialogVisible = () => {
        isOpen.value = true
    }

    const handlerClose = (res) => {
        isOpen.value = res
    }

</script>

<style lang='scss' scoped>
    .navbar {
        height: 51px;
        overflow: hidden;
        position: relative;
        background: #fff;
        width: 100%;
        // display: flex;
        // box-shadow: 1px 1px 4px rgba(0, 21, 41, 0.11);
        box-shadow: 0px 0px 5px rgba(0, 21, 41, 0.11);
        border-bottom: 1px solid #eee;

        .left-menu {
            float: left;
            height: 100%;
            line-height: 50px;
            display: flex;
        }

        .hamburger-container {
            line-height: 46px;
            height: 100%;
            float: left;
            cursor: pointer;
            background-color: rgba(0, 0, 0, 0.025);
            transition: background 0.3s;
            -webkit-tap-highlight-color: transparent;

            &:hover {
                background: rgba(0, 0, 0, 0.035);
            }
        }

        .breadcrumb-container {
            float: left;
        }

        .topmenu-container {
            float: left;
            // position: absolute;
            // left: 50px;
        }

        .errLog-container {
            display: inline-block;
            vertical-align: top;
        }

        .right-menu {
            float: right;
            height: 100%;
            line-height: 50px;
            display: flex;

            &:focus {
                outline: none;
            }

            .right-menu-item {
                display: inline-block;
                padding: 0 13px;
                height: 100%;
                font-size: 18px;
                color: #344563;
                vertical-align: text-bottom;

                &.hover-effect {
                    cursor: pointer;
                    transition: background 0.3s;

                    &:hover {
                        background: rgba(0, 0, 0, 0.025);
                    }
                }
            }

            .avatar-container {
                margin-right: 10px;

                .el-dropdown-menu__item {
                    padding: 5px 26px
                }

                .avatar-wrapper {
                    margin-top: 10px;
                    position: relative;

                    .user-avatar {
                        cursor: pointer;
                        width: 26px;
                        height: 26px;
                        border-radius: 50%;
                    }

                    i {
                        cursor: pointer;
                        position: absolute;
                        right: 8px;
                        top: 25px;
                        font-size: 12px;
                    }
                }
            }
        }
    }
</style>
