<template>
    <div id="app">
        <keep-alive>
            <router-view v-if="$route.meta.keepAlive"></router-view>
        </keep-alive>
        <router-view class="router-view" v-if="!$route.meta.keepAlive"/>
    </div>
</template>

<script setup>
    import useSettingsStore from '@/store/modules/settings'
    import {handleThemeStyle} from '@/utils/theme'

    onMounted(() => {
        nextTick(() => {
            // 初始化主题样式
            handleThemeStyle(useSettingsStore().theme)
            addDocumentVisibilityChange()
        })
    })

    /**
     * @description: 当前标签再次显现进行的处理逻辑
     * @param {*}
     * @return {*}
     */
    const addDocumentVisibilityChange = () => {
        // 网页当前状态判断
        var state, visibilityChange
        if (typeof document.hidden !== 'undefined') {
            // hidden = 'hidden'
            visibilityChange = 'visibilitychange'
            state = 'visibilityState'
        } else if (typeof document.mozHidden !== 'undefined') {
            // hidden = 'mozHidden'
            visibilityChange = 'mozvisibilitychange'
            state = 'mozVisibilityState'
        } else if (typeof document.msHidden !== 'undefined') {
            // hidden = 'msHidden'
            visibilityChange = 'msvisibilitychange'
            state = 'msVisibilityState'
        } else if (typeof document.webkitHidden !== 'undefined') {
            // hidden = 'webkitHidden'
            visibilityChange = 'webkitvisibilitychange'
            state = 'webkitVisibilityState'
        }
        // 添加监听器，在title里显示状态变化
        document.addEventListener(visibilityChange, () => {
            if (document[state] == 'visible') {
                // if (this.route.name === 'login') {
                window.location.reload()
                // }
            }
        }, false)
    }

</script>

<style lang="scss">
    #app {
        position: relative;
        display: flex;
        flex-direction: column;
        width: 100%;
        min-width: 1200px;
        height: 100%;
        min-height: 605px;
    }
</style>
