import { type App } from 'vue'
import AppIcon from './icons/AppIcon.vue'
import AppAvatar from './app-avatar/index.vue'
import LoginLayout from './login-layout/index.vue'
import LoginContainer from './login-container/index.vue'
import LayoutContainer from './layout-container/index.vue'
import TagsInput from './tags-input/index.vue'
import CardBox from './card-box/index.vue'
import CardBoxNew from './card-box-new/index.vue'
import CardAdd from './card-add/index.vue'
import BackButton from './back-button/index.vue'
import AppTable from './app-table/index.vue'
import ReadWrite from './read-write/index.vue'
import TagEllipsis from './tag-ellipsis/index.vue'
import CommonList from './common-list/index.vue'
import MarkdownRenderer from './markdown-renderer/index.vue'
import dynamicsForm from './dynamics-form'
import CardCheckbox from './card-checkbox/index.vue'
import AiChat from './ai-chat/index.vue'
import InfiniteScroll from './infinite-scroll/index.vue'
import AutoTooltip from './auto-tooltip/index.vue'

export default {
  install(app: App) {
    app.component(AppIcon.name, AppIcon)
    app.component(AppAvatar.name, AppAvatar)
    app.component(LoginLayout.name, LoginLayout)
    app.component(LoginContainer.name, LoginContainer)
    app.component(LayoutContainer.name, LayoutContainer)
    app.component(TagsInput.name, TagsInput)
    app.component(CardBox.name, CardBox)
    app.component(CardBoxNew.name, CardBoxNew)
    app.component(CardAdd.name, CardAdd)
    app.component(BackButton.name, BackButton)
    app.component(AppTable.name, AppTable)
    app.component(ReadWrite.name, ReadWrite)
    app.component(TagEllipsis.name, TagEllipsis)
    app.component(CommonList.name, CommonList)
    app.use(dynamicsForm)
    app.component(MarkdownRenderer.name, MarkdownRenderer)
    app.component(CardCheckbox.name, CardCheckbox)
    app.component(AiChat.name, AiChat)
    app.component(InfiniteScroll.name, InfiniteScroll)
    app.component(AutoTooltip.name, AutoTooltip)
  }
}
