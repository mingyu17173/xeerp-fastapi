<template>
    <div>
        <button class="but-buttom is-circle">
            <el-icon size="23" @click="openTags">
                <switch-filled/>
            </el-icon>
        </button>
    </div>
</template>

<script setup>
    import useSettingsStore from '@/store/modules/settings'

    const settingsStore = useSettingsStore()

    const tagsView = computed(() => settingsStore.tagsView);
    const storeSettings = computed(() => settingsStore);

    function openTags(e) {
        e.preventDefault();
        if (tagsView.value) {
            settingsStore.tagsView = false
        } else {
            settingsStore.tagsView = true
        }

        let layoutSetting = {
            "topNav": storeSettings.value.topNav,
            "tagsView": storeSettings.value.tagsView,
            "fixedHeader": storeSettings.value.fixedHeader,
            "sidebarLogo": storeSettings.value.sidebarLogo,
            "dynamicTitle": storeSettings.value.dynamicTitle,
            "sideTheme": storeSettings.value.sideTheme,
            "theme": storeSettings.value.theme
        };

        localStorage.setItem("layout-setting", JSON.stringify(layoutSetting));
    }


</script>