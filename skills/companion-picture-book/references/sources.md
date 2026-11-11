# 来源与适配范围

核实日期：2026-10-15。

## 用户需求

读取了用户需求对话，其中的需求包括适龄建议、照片建议、故事／单页分支、梗概和风格确认、质量检查，以及后续补充的中英双语融入画面和三份 TXT。2026-10-16 的用户修订要求将双语对照稿加入音标与中文谐音（用户所称罗马音），并额外拆出两份英文教学稿，当前默认交付共五份 TXT。用户在对话中明确取消了点读笔品牌及设备适配要求。

「暖阳手绘」依据该对话里可见的文字定义整理；原参考图、孩子照片和旧作品不包含在本技能包中，未来制作不能假装已获得这些素材。旧例子的六页、奶油色裙子和家庭角色不是新作品的默认固定设定。

## 第一套 Codex 绘本生成器

用户所指的第一套是 [kangqiang1996-bot/picture-book-generator](https://github.com/kangqiang1996-bot/picture-book-generator)，采用 MIT 许可。本技能根据以下文件中的方法重新组织适配流程，并保留相关许可：

- [SKILL.md](https://github.com/kangqiang1996-bot/picture-book-generator/blob/main/SKILL.md)：制作顺序、场景／道具状态、逐页生成、排版与局部修复。
- [quality checklist](https://github.com/kangqiang1996-bot/picture-book-generator/blob/main/references/qa-checklist.md)：故事、适龄、视觉、文字和交付检查。
- [character continuity](https://github.com/kangqiang1996-bot/picture-book-generator/blob/main/references/character-continuity.md)：固定角色特征、视觉锚点、手部归属、镜头与风格一致性。
- [story structure](https://github.com/kangqiang1996-bot/picture-book-generator/blob/main/references/story-structure.md)：故事拆页和每页叙事作用。

本版补充了年龄与观察驱动的推荐、照片选择、双分支、实际面容对照、双语主文稿与纯文本导出、用户确认状态及有限次数返工。未引入上游商业发布或 KDP 流程。原项目的 3–8 岁、12 页和三语版式默认值没有覆盖本任务的适龄选择和中英双语要求。

参见 [上游 MIT 许可](../LICENSE.picture-book-generator)。

## 年龄参考

可核查的 AAP 和 CDC 来源及其支持范围列于 [适龄评估与照片建议](age-and-materials.md)。页数、角色数、风格、照片需求和分流方案属于创作设计，并非上述机构认证的分级标准。
