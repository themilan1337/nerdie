export const useSidebar = () => {
    const isSidebarExpanded = useCookie<boolean>('sidebar-expanded', {
        default: () => true,
        watch: true,
        maxAge: 60 * 60 * 24 * 365, // 1 year
    })

    const toggleSidebar = () => {
        isSidebarExpanded.value = !isSidebarExpanded.value
    }

    const expandSidebar = () => {
        isSidebarExpanded.value = true
    }

    const collapseSidebar = () => {
        isSidebarExpanded.value = false
    }

    return {
        isSidebarExpanded,
        toggleSidebar,
        expandSidebar,
        collapseSidebar,
    }
}
