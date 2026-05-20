<template>
    <div :style="styles" class="vux-flexbox-item">
        <slot/>
    </div>
</template>

<script setup>
    import {onBeforeMount} from 'vue'

    const prefixList = ['-moz-box-', '-webkit-box-', '']

    const props = defineProps({
        span: [Number, String],
        order: [Number, String]
    });

    const bodyWidth = ref(0)

    const styles = () => {
        const styles = {}
        const marginName =
            $parent.orient === 'horizontal' ? 'marginLeft' : 'marginTop'

        if (this.$parent.gutter * 1 !== 0) {
            styles[marginName] = `${$parent.gutter}px`
        }

        if (this.span) {
            for (let i = 0; i < prefixList.length; i++) {
                styles[`${prefixList[i]}flex`] = `0 0 ${buildWidth(this.span) *
                100}%`
            }
        }

        if (typeof this.order !== 'undefined') {
            styles.order = this.order
        }

        return styles
    }

    onBeforeMount(() => {
        bodyWidth.value = document.documentElement.offsetWidth;
    });


    const buildWidth = (width) => {
        if (typeof width == 'number') {
            if (width < 1) {
                return width
            } else {
                return width / 12
            }
        } else if (typeof width === 'string') {
            return width.replace('px', '') / bodyWidth.value
        }
    }
</script>