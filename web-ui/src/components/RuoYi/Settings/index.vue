<template>
    <div>
        <button class="but-buttom is-circle">
            <el-icon size="21" @click="handleSelect">
                <setting/>
            </el-icon>
        </button>
    </div>
</template>

<script setup>
    import useSettingsStore from '@/store/modules/settings'
    import {constantRoutes} from "@/router"
    import {isHttp} from '@/utils/validate'
    import useAppStore from '@/store/modules/app'
    import usePermissionStore from '@/store/modules/permission'

    const settingsStore = useSettingsStore()
    const permissionStore = usePermissionStore()
    const appStore = useAppStore()
    const route = useRoute();
    const router = useRouter();

    // 所有的路由信息
    const routers = computed(() => permissionStore.topbarRouters);
    const tagsView = computed(() => settingsStore.tagsView);
    const storeSettings = computed(() => settingsStore);


    // 顶部栏初始数
    const visibleNumber = ref(null);
    // 当前激活菜单的 index
    const currentIndex = ref(null);
    // 隐藏侧边栏路由
    const hideList = ['/index', '/user/profile'];


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

    // 设置子路由
    const childrenMenus = computed(() => {
        let childrenMenus = [];
        routers.value.map((router) => {
            for (let item in router.children) {
                if (router.children[item].parentPath === undefined) {
                    if (router.path === "/") {
                        router.children[item].path = "/" + router.children[item].path;
                    } else {
                        if (!isHttp(router.children[item].path)) {
                            router.children[item].path = router.path + "/" + router.children[item].path;
                        }
                    }
                    router.children[item].parentPath = router.path;
                }
                childrenMenus.push(router.children[item]);
            }
        })
        return constantRoutes.concat(childrenMenus);
    })


    function handleSelect() {
        let key = "/system"
        let keyPath = ["/system"]

        currentIndex.value = key;
        const route = routers.value.find(item => item.path === key);

        if (isHttp(key)) {
            // http(s):// 路径新窗口打开
            window.open(key, "_blank");
        } else if (!route || !route.children) {
            // 没有子路由路径内部打开
            const routeMenu = childrenMenus.value.find(item => item.path === key);
            if (routeMenu && routeMenu.query) {
                let query = JSON.parse(routeMenu.query);
                router.push({path: key, query: query});
            } else {
                router.push({path: key});
            }
            appStore.toggleSideBarHide(true);
        } else {
            // 显示左侧联动菜单
            activeRoutes(key);
            appStore.toggleSideBarHide(false);
        }
    }

    function activeRoutes(key) {
        let routes = [];
        if (childrenMenus.value && childrenMenus.value.length > 0) {
            childrenMenus.value.map((item) => {
                if (key == item.parentPath || (key == "index" && "" == item.path)) {
                    routes.push(item);
                }
            });
        }
        if (routes.length > 0) {
            permissionStore.setSidebarRouters(routes);
        } else {
            appStore.toggleSideBarHide(true);
        }
        return routes;
    }


</script>