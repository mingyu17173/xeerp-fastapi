<template>
    <div class="sidebar-logo-min" :class="{ 'collapse': collapse }">
        <transition name="sidebarLogoFade">
            <router-link v-if="collapse" key="collapse" class="sidebar-logo-link" to="/">
                <img v-if="logo" :src="logo" class="sidebar-logo" :title="title"/>
            </router-link>
            <router-link v-else key="expand" class="sidebar-logo-link" to="/">
                <img v-if="logo" :src="logo" class="sidebar-logo" :title="title"/>
            </router-link>
        </transition>
    </div>
</template>

<script setup>
    import logo from '@/assets/logo/logo.jpg'
    import useSettingsStore from '@/store/modules/settings'

    defineProps({
        collapse: {
            type: Boolean,
            required: true
        }
    })

    const title = import.meta.env.VITE_APP_TITLE;
    const settingsStore = useSettingsStore();
</script>

<style lang="scss" scoped>
    .sidebar-logo-min {
        position: relative;
        width: 60px;
        height: 50px;
        line-height: 50px;
        background: #fff;
        text-align: center;
        float: left;
        overflow: hidden;

        & .sidebar-logo-link {
            height: 100%;
            width: 100%;

            & .sidebar-logo {
                width: 32px;
                height: 32px;
                vertical-align: middle;
                margin: 0px 12px;
                border-radius: 3px;
                margin-top: -2px;
            }

            & .sidebar-title {
                display: inline-block;
                margin: 0;
                color: #fff;
                font-weight: 600;
                line-height: 50px;
                font-size: 14px;
                font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
                vertical-align: middle;
            }
        }

        &.collapse {
            .sidebar-logo {
                margin-right: 0px;
            }
        }
    }
</style>