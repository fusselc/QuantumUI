import React, { useState, useEffect } from 'react';
import { api } from './api/client';
import {
  Template,
  ExperimentRecord,
  ProviderInfo
} from './types';
import { StatusBadge } from './components/StatusBadge';
import { PromptBox } from './components/PromptBox';
import { TemplateCard } from './components/TemplateCard';
import { CircuitVisualizer } from './components/CircuitVisualizer';
import { CodePanel } from './components/CodePanel';
import { ExecutionControlBar } from './components/ExecutionControlBar';
import { ResultPanel } from './components/ResultPanel';
import { SharingPanel } from './components/SharingPanel';
import { Atom, Shield, AlertCircle } from 'lucide-react';

export const App: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [providers, setProviders] = useState<ProviderInfo[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [promptText, setPromptText] = useState('');
  const [experiment, setExperiment] = useState<ExperimentRecord | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Load initial templates and provider list
  useEffect(() => {
    async function loadInitial() {
      try {
        const [tpls, provs] = await Promise.all([
          api.getTemplates(),
          api.getProviders()
        ]);
        setTemplates(tpls);
        setProviders(provs);
        if (tpls.length > 0) {
          handleSelectTemplate(tpls[0]);
        }
      } catch (err: any) {
        console.error('Initialization error:', err);
      }
    }
    loadInitial();
  }, []);

  const handleSelectTemplate = async (tpl: Template) => {
    setSelectedTemplate(tpl);
    setPromptText(tpl.prompt_text);
    setErrorMessage(null);
    setLoading(true);
    try {
      const exp = await api.createExperiment({ template_id: tpl.template_id });
      setExperiment(exp);
    } catch (err: any) {
      setErrorMessage(err.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePrompt = async () => {
    if (!promptText.trim()) return;
    setErrorMessage(null);
    setLoading(true);
    try {
      const exp = await api.createExperiment({ prompt_text: promptText });
      setExperiment(exp);
      setSelectedTemplate(null);
    } catch (err: any) {
      setErrorMessage(err.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCodeChange = (newCode: string) => {
    if (experiment) {
      setExperiment({
        ...experiment,
        user_edited_code: newCode
      });
    }
  };

  const handleValidateCode = async () => {
    if (!experiment) return;
    const codeToValidate = experiment.user_edited_code || experiment.generated_code;
    setLoading(true);
    try {
      const updated = await api.validateCode(experiment.experiment_id, codeToValidate);
      setExperiment(updated);
    } catch (err: any) {
      setErrorMessage(err.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = async (hwToken?: string) => {
    if (!experiment) return;
    setErrorMessage(null);
    setLoading(true);
    try {
      const updated = await api.executeExperiment(
        experiment.experiment_id,
        experiment.execution_config,
        hwToken
      );
      setExperiment(updated);
    } catch (err: any) {
      setErrorMessage(err.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateSharing = async (partial: Partial<ExperimentRecord['sharing_state']>) => {
    if (!experiment) return;
    try {
      const updated = await api.updateSharing(experiment.experiment_id, partial);
      setExperiment(updated);
    } catch (err: any) {
      setErrorMessage(err.detail || err.message);
    }
  };

  const handleExportNotebook = () => {
    if (!experiment) return;
    window.open(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/v1'}/experiments/${experiment.experiment_id}/export/notebook`, '_blank');
  };

  const handleOpenColab = async () => {
    if (!experiment) return;
    try {
      const res = await api.getColabUrl(experiment.experiment_id);
      window.open(res.colab_url, '_blank');
    } catch (err: any) {
      setErrorMessage(err.detail || err.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 font-sans">
      {/* Top Navigation */}
      <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-tr from-cyan-500 to-sky-600 rounded-lg shadow-lg shadow-cyan-500/20">
            <Atom className="w-5 h-5 text-black font-bold" />
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-100 tracking-tight flex items-center gap-2">
              QuantumUI <span className="text-xs text-cyan-400 font-mono font-normal border border-cyan-800/60 bg-cyan-950/60 px-1.5 py-0.5 rounded">v1.0-MVP</span>
            </h1>
            <p className="text-[11px] text-slate-400">No-Code Quantum Cloud Gateway & Experimenter</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {experiment && <StatusBadge status={experiment.execution_result.status} />}
        </div>
      </header>

      {/* Error Alert */}
      {errorMessage && (
        <div className="mx-6 mt-4 p-3 rounded-lg bg-rose-950/80 border border-rose-800 text-xs text-rose-200 flex items-center gap-2 shadow-lg animate-fade-in">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
          <span className="flex-1">{errorMessage}</span>
          <button type="button" onClick={() => setErrorMessage(null)} className="text-rose-400 hover:text-rose-100 text-xs font-bold">✕</button>
        </div>
      )}

      {/* Main Workspace (12-Column Responsive Grid) */}
      <main className="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto w-full">
        {/* Left Column: Templates Catalog & Guided Prompt (5 Cols) */}
        <section className="lg:col-span-5 flex flex-col gap-4">
          <PromptBox
            promptText={promptText}
            onPromptChange={setPromptText}
            onSubmit={handleGeneratePrompt}
            suggestionChips={selectedTemplate?.suggestion_chips || []}
            isLoading={loading}
          />

          <div className="flex items-center justify-between pt-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Foundational Templates
            </h2>
            <span className="text-[11px] text-slate-500">Phase 1 Baseline</span>
          </div>

          <div className="grid grid-cols-1 gap-2.5">
            {templates.map((tpl) => (
              <TemplateCard
                key={tpl.template_id}
                template={tpl}
                isSelected={selectedTemplate?.template_id === tpl.template_id}
                onSelect={handleSelectTemplate}
              />
            ))}
          </div>
        </section>

        {/* Right Column: Visual Circuit, Code, Execution & Results (7 Cols) */}
        <section className="lg:col-span-7 flex flex-col gap-4">
          <CircuitVisualizer
            code={experiment ? (experiment.user_edited_code || experiment.generated_code) : ''}
            circuitDescription={experiment?.circuit_description}
          />

          <CodePanel
            code={experiment ? (experiment.user_edited_code || experiment.generated_code) : ''}
            isUserEdited={Boolean(experiment?.user_edited_code)}
            onCodeChange={handleCodeChange}
            onValidate={handleValidateCode}
            validationReport={experiment?.validation_report}
            isLoading={loading}
          />

          {experiment && (
            <ExecutionControlBar
              config={experiment.execution_config}
              providers={providers}
              onConfigChange={(newCfg) => setExperiment({ ...experiment, execution_config: newCfg })}
              onExecute={handleExecute}
              isLoading={loading}
            />
          )}

          <ResultPanel
            result={experiment?.execution_result}
            explanation={experiment?.explanation_by_level}
          />

          {experiment && (
            <SharingPanel
              experimentId={experiment.experiment_id}
              sharingState={experiment.sharing_state}
              onUpdateSharing={handleUpdateSharing}
              onExportNotebook={handleExportNotebook}
              onOpenColab={handleOpenColab}
            />
          )}
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/60 py-4 px-6 text-center text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-2">
        <span>QuantumUI • Open Source Gateway under MIT & CC BY 4.0</span>
        <span className="flex items-center gap-1">
          <Shield className="w-3.5 h-3.5 text-cyan-400" />
          Strict Educational Safety Policy Enforced
        </span>
      </footer>
    </div>
  );
};
