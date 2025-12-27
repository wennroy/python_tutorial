/**
 * Python Tutorial Platform - Frontend Application
 * Vue.js 3 application for interactive tutorial display
 */

const { createApp, ref, reactive, computed, onMounted, watch } = Vue;

// API Base URL - Change this for production
const API_BASE = 'http://localhost:8000';

const app = createApp({
    setup() {
        // ============== State ==============
        const curriculum = reactive({ modules: [] });
        const currentModule = ref(null);
        const currentChapter = ref(null);
        const chapterContent = ref('');
        const userCode = ref('');
        const solutionCode = ref('');
        const currentExerciseFile = ref('');
        
        // UI State
        const sidebarCollapsed = ref(false);
        const expandedModules = reactive({});
        const showCodePanel = ref(false);
        const showDiff = ref(false);
        const loading = ref(false);
        const error = ref(null);
        
        // Code editing state
        const codeModified = ref(false);
        const codeSaveStatus = ref(''); // 'success', 'error', ''
        const codeSaveMessage = ref('');
        const originalCode = ref('');
        
        // DOM References
        const tutorialContentRef = ref(null);
        
        // Current chapter index for navigation
        const currentChapterIndex = ref(-1);
        const currentModuleIndex = ref(-1);

        // ============== API Methods ==============
        
        /**
         * Fetch curriculum structure from backend
         */
        async function fetchCurriculum() {
            try {
                const response = await fetch(`${API_BASE}/api/curriculum`);
                if (!response.ok) throw new Error('Failed to fetch curriculum');
                const data = await response.json();
                curriculum.modules = data.modules;
                
                // Expand first module by default
                if (curriculum.modules.length > 0) {
                    expandedModules[curriculum.modules[0].id] = true;
                }
            } catch (err) {
                console.error('Error fetching curriculum:', err);
                error.value = 'Failed to load curriculum. Is the backend running?';
            }
        }

        /**
         * Load a specific chapter's content
         */
        async function loadChapter(moduleId, chapter) {
            loading.value = true;
            error.value = null;
            
            try {
                const response = await fetch(`${API_BASE}/api/chapter/${moduleId}/${chapter.id}`);
                if (!response.ok) throw new Error('Failed to fetch chapter');
                const data = await response.json();
                
                chapterContent.value = data.content;
                currentChapter.value = chapter;
                currentModule.value = curriculum.modules.find(m => m.id === moduleId);
                
                // Update indices for navigation
                currentModuleIndex.value = curriculum.modules.findIndex(m => m.id === moduleId);
                if (currentModuleIndex.value >= 0) {
                    currentChapterIndex.value = curriculum.modules[currentModuleIndex.value].chapters.findIndex(c => c.id === chapter.id);
                }
                
                // Update exercise file name based on chapter
                const exerciseMatch = chapter.id.match(/(\d+)/);
                if (exerciseMatch) {
                    currentExerciseFile.value = `exercise_${moduleId.replace(/\D/g, '').padStart(2, '0')}_${exerciseMatch[1].padStart(2, '0')}.py`;
                }
                
                // Save progress to localStorage
                saveProgress(moduleId, chapter.id);
                
                // Apply syntax highlighting after content is rendered
                setTimeout(() => {
                    document.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightElement(block);
                    });
                }, 100);
                
            } catch (err) {
                console.error('Error loading chapter:', err);
                error.value = 'Failed to load chapter content.';
            } finally {
                loading.value = false;
            }
        }

        /**
         * Fetch user's code from workspace
         */
        async function fetchUserCode() {
            if (!currentExerciseFile.value) return;
            
            try {
                const response = await fetch(`${API_BASE}/api/code/${currentExerciseFile.value}`);
                if (!response.ok) {
                    // File not found - create a template
                    const template = `# ${currentExerciseFile.value}\n# 请在这里编写你的代码\n\n`;
                    userCode.value = template;
                    originalCode.value = '';
                    codeModified.value = true; // Mark as modified so user can save
                    return;
                }
                const data = await response.json();
                userCode.value = data.content;
                originalCode.value = data.content;
                codeModified.value = false;
                
            } catch (err) {
                console.error('Error fetching user code:', err);
                userCode.value = '# Error loading code file';
                originalCode.value = '';
            }
        }

        /**
         * Fetch solution code for comparison
         */
        async function fetchSolution() {
            if (!currentModule.value || !currentExerciseFile.value) return;
            
            const exerciseId = currentExerciseFile.value.replace('.py', '');
            try {
                const response = await fetch(`${API_BASE}/api/solution/${currentModule.value.id}/${exerciseId}`);
                if (!response.ok) {
                    solutionCode.value = '// Solution not available';
                    return;
                }
                const data = await response.json();
                solutionCode.value = data.solution;
                
            } catch (err) {
                console.error('Error fetching solution:', err);
                solutionCode.value = '// Error loading solution';
            }
        }

        // ============== UI Methods ==============

        /**
         * Toggle module expansion in sidebar
         */
        function toggleModule(moduleId) {
            expandedModules[moduleId] = !expandedModules[moduleId];
        }

        /**
         * Toggle code panel visibility
         */
        function toggleCodePanel() {
            showCodePanel.value = !showCodePanel.value;
            if (showCodePanel.value) {
                fetchUserCode();
                fetchSolution();
            }
        }

        /**
         * Refresh user code from file
         */
        function refreshCode() {
            fetchUserCode();
        }

        /**
         * Handle code change in editor
         */
        function onCodeChange() {
            codeModified.value = userCode.value !== originalCode.value;
            // Clear save status when editing
            if (codeSaveStatus.value) {
                codeSaveStatus.value = '';
                codeSaveMessage.value = '';
            }
        }

        /**
         * Handle Tab key in editor (insert spaces instead of losing focus)
         */
        function handleTab(event) {
            const textarea = event.target;
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            
            // Insert 4 spaces at cursor position
            userCode.value = userCode.value.substring(0, start) + '    ' + userCode.value.substring(end);
            
            // Move cursor after inserted spaces
            setTimeout(() => {
                textarea.selectionStart = textarea.selectionEnd = start + 4;
            }, 0);
            
            onCodeChange();
        }

        /**
         * Save code to file
         */
        async function saveCode() {
            if (!currentExerciseFile.value) return;
            
            try {
                const response = await fetch(`${API_BASE}/api/code/save`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        filename: currentExerciseFile.value,
                        content: userCode.value
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to save file');
                }
                
                const data = await response.json();
                originalCode.value = userCode.value;
                codeModified.value = false;
                codeSaveStatus.value = 'success';
                codeSaveMessage.value = '已保存';
                
                // Clear success message after 2 seconds
                setTimeout(() => {
                    codeSaveStatus.value = '';
                    codeSaveMessage.value = '';
                }, 2000);
                
            } catch (err) {
                console.error('Error saving code:', err);
                codeSaveStatus.value = 'error';
                codeSaveMessage.value = '保存失败';
            }
        }

        // ============== Navigation Methods ==============
        
        /**
         * Check if there's a previous chapter available
         */
        const hasPrevChapter = computed(() => {
            if (currentModuleIndex.value < 0 || currentChapterIndex.value < 0) return false;
            
            // Has previous chapter in same module
            if (currentChapterIndex.value > 0) return true;
            
            // Has previous module with chapters
            if (currentModuleIndex.value > 0) {
                const prevModule = curriculum.modules[currentModuleIndex.value - 1];
                return prevModule && prevModule.chapters.length > 0;
            }
            
            return false;
        });
        
        /**
         * Check if there's a next chapter available
         */
        const hasNextChapter = computed(() => {
            if (currentModuleIndex.value < 0 || currentChapterIndex.value < 0) return false;
            
            const currentMod = curriculum.modules[currentModuleIndex.value];
            if (!currentMod) return false;
            
            // Has next chapter in same module
            if (currentChapterIndex.value < currentMod.chapters.length - 1) return true;
            
            // Has next module with chapters
            if (currentModuleIndex.value < curriculum.modules.length - 1) {
                const nextModule = curriculum.modules[currentModuleIndex.value + 1];
                return nextModule && nextModule.chapters.length > 0;
            }
            
            return false;
        });
        
        /**
         * Navigate to previous chapter
         */
        function goToPrevChapter() {
            if (!hasPrevChapter.value) return;
            
            let newModuleIndex = currentModuleIndex.value;
            let newChapterIndex = currentChapterIndex.value - 1;
            
            // Move to previous module if needed
            if (newChapterIndex < 0) {
                newModuleIndex--;
                const prevModule = curriculum.modules[newModuleIndex];
                newChapterIndex = prevModule.chapters.length - 1;
            }
            
            const targetModule = curriculum.modules[newModuleIndex];
            const targetChapter = targetModule.chapters[newChapterIndex];
            
            expandedModules[targetModule.id] = true;
            loadChapter(targetModule.id, targetChapter);
        }
        
        /**
         * Navigate to next chapter
         */
        function goToNextChapter() {
            if (!hasNextChapter.value) return;
            
            let newModuleIndex = currentModuleIndex.value;
            let newChapterIndex = currentChapterIndex.value + 1;
            
            const currentMod = curriculum.modules[newModuleIndex];
            
            // Move to next module if needed
            if (newChapterIndex >= currentMod.chapters.length) {
                newModuleIndex++;
                newChapterIndex = 0;
            }
            
            const targetModule = curriculum.modules[newModuleIndex];
            const targetChapter = targetModule.chapters[newChapterIndex];
            
            expandedModules[targetModule.id] = true;
            loadChapter(targetModule.id, targetChapter);
        }
        
        /**
         * Scroll tutorial content to top
         */
        function scrollToTop() {
            const content = document.querySelector('.tutorial-content');
            console.log('scrollToTop called, content:', content);
            if (content) {
                content.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }
        
        /**
         * Scroll tutorial content to bottom
         */
        function scrollToBottom() {
            const content = document.querySelector('.tutorial-content');
            console.log('scrollToBottom called, content:', content, 'scrollHeight:', content?.scrollHeight);
            if (content) {
                content.scrollTo({ top: content.scrollHeight, behavior: 'smooth' });
            }
        }
        
        /**
         * Toggle solution comparison (opens code panel and shows diff)
         */
        function toggleSolutionCompare() {
            if (!showCodePanel.value) {
                showCodePanel.value = true;
                fetchUserCode();
                fetchSolution();
                showDiff.value = true;
            } else if (!showDiff.value) {
                showDiff.value = true;
            } else {
                showDiff.value = false;
                showCodePanel.value = false;
            }
        }

        // ============== Progress Tracking ==============

        /**
         * Save reading progress to localStorage
         */
        function saveProgress(moduleId, chapterId) {
            const progress = JSON.parse(localStorage.getItem('tutorialProgress') || '{}');
            progress.lastModule = moduleId;
            progress.lastChapter = chapterId;
            progress.completedChapters = progress.completedChapters || [];
            
            const key = `${moduleId}/${chapterId}`;
            if (!progress.completedChapters.includes(key)) {
                progress.completedChapters.push(key);
            }
            
            localStorage.setItem('tutorialProgress', JSON.stringify(progress));
        }

        /**
         * Load saved progress from localStorage
         */
        function loadProgress() {
            const progress = JSON.parse(localStorage.getItem('tutorialProgress') || '{}');
            return progress;
        }

        // ============== Lifecycle ==============

        onMounted(async () => {
            await fetchCurriculum();
            
            // Load last viewed chapter if available
            const progress = loadProgress();
            if (progress.lastModule && progress.lastChapter) {
                const module = curriculum.modules.find(m => m.id === progress.lastModule);
                if (module) {
                    const chapter = module.chapters.find(c => c.id === progress.lastChapter);
                    if (chapter) {
                        expandedModules[module.id] = true;
                        loadChapter(module.id, chapter);
                    }
                }
            }
        });

        // Watch for code panel visibility to refresh
        watch(showDiff, (newVal) => {
            if (newVal) {
                setTimeout(() => {
                    document.querySelectorAll('.diff-view pre code').forEach((block) => {
                        hljs.highlightElement(block);
                    });
                }, 100);
            }
        });

        return {
            // State
            curriculum,
            currentModule,
            currentChapter,
            chapterContent,
            userCode,
            solutionCode,
            currentExerciseFile,
            sidebarCollapsed,
            expandedModules,
            showCodePanel,
            showDiff,
            loading,
            error,
            
            // Code editing state
            codeModified,
            codeSaveStatus,
            codeSaveMessage,
            
            // Methods
            toggleModule,
            loadChapter,
            toggleCodePanel,
            refreshCode,
            onCodeChange,
            handleTab,
            saveCode,
            
            // Navigation
            tutorialContentRef,
            hasPrevChapter,
            hasNextChapter,
            goToPrevChapter,
            goToNextChapter,
            scrollToTop,
            scrollToBottom,
            toggleSolutionCompare
        };
    }
});

app.mount('#app');
