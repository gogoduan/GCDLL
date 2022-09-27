import { shallowMount, createLocalVue } from '@vue/test-utils'
import SearchBar from '@/components/SearchBar.vue'
import ElementUI from 'element-ui';

const localVue = createLocalVue()
localVue.use(ElementUI)
// const element = new ElementUI()

const factory = (values = {}) => {
    return shallowMount(SearchBar, {
      localVue,
      // element,
      data () {
        return {
          ...values
        }
      }
    })
  }
  
  describe('SearchBar', () => {
    it('check exist', () => {
      const wrapper = factory()
      const div = wrapper.find('div')
      expect(div.exists()).toBe(true)
      const bar = wrapper.find('.search-bar')
      expect(bar.exists()).toBe(true)
      const search = wrapper.find('#search')
      expect(search.exists()).toBe(true)
    })
  })
